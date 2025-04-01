import copy
import json
import pathlib
import shutil
import textwrap
import time
import urllib.parse
from typing import Generator

import yaml

from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
    AssetsDefinition,
)
from OpenStudioLandscapes.engine.base.assets import KEY_BASE
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.base.ops import (
    op_compose,
    op_docker_compose_graph,
    op_group_out,
)

from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.whales import *

from OpenStudioLandscapes.Dagster.constants import *


# Todo:
#  - [ ] Create dagster.yaml dynamically


@asset(
    **ASSET_HEADER,
    ins={
        "group_in": AssetIn(
            AssetKey([*KEY_BASE, "group_out"])
        ),
    },
    deps=[
        AssetKey([*ASSET_HEADER['key_prefix'], "constants"])
    ],
)
def env(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:

    env_in = copy.deepcopy(group_in["env"])

    # Todo
    #  - [ ] externalize
    # expanding variables in OpenStudioLandscapes.Kitsu.constants.ENVIRONMENT
    for k, v in ENVIRONMENT.items():
        if isinstance(v, str):
            ENVIRONMENT[k] = v.format(**env_in)

    env_in.update(ENVIRONMENT)

    env_in.update(
        {
            "COMPOSE_SCOPE": COMPOSE_SCOPE,
        },
    )

    yield Output(env_in)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(env_in),
            "ENVIRONMENT": MetadataValue.json(ENVIRONMENT),
        },
    )


@asset(
    **ASSET_HEADER,
)
def pip_packages(
    context: AssetExecutionContext,
) -> Generator[Output[list] | AssetMaterialization, None, None]:
    """ """

    # Todo
    #  Check: content seems identical to asset `pip_packages_base_image`
    _pip_packages: list = [
        # "dagster-shared[dev] @ git+https://github.com/michimussato/dagster-shared.git@main",
        # "deadline-dagster[dev] @ git+https://github.com/michimussato/deadline-dagster.git@main",
    ]

    if DAGSTER_USE_POSTGRES:
        _pip_packages.append(
            "dagster-postgres==0.25.11"
        )

    yield Output(_pip_packages)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_pip_packages),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "group_in": AssetIn(
            AssetKey([*KEY_BASE, "group_out"])
        ),
        "pip_packages": AssetIn(
            AssetKey([*KEY, "pip_packages"]),
        ),
    },
)
def build_docker_image(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    group_in: dict,  # pylint: disable=redefined-outer-name
    pip_packages: list,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    build_base_image_data: dict = group_in["docker_image"]
    build_base_docker_config: DockerConfig = group_in["docker_config"]

    if build_base_docker_config.value["docker_push"]:
        build_base_parent_image_prefix: str = build_base_image_data["image_prefix_full"]
    else:
        build_base_parent_image_prefix: str = build_base_image_data["image_prefix_local"]

    build_base_parent_image_name: str = build_base_image_data["image_name"]
    build_base_parent_image_tags: list = build_base_image_data["image_tags"]

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{GROUP}__{'__'.join(KEY)}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    docker_file.parent.mkdir(parents=True, exist_ok=True)

    image_name = get_image_name(context=context)
    # image_path = parse_docker_image_path(
    #     image_name=image_name,
    #     docker_config=build_base_docker_config,
    # )
    image_prefix_local = parse_docker_image_path(
        docker_config=build_base_docker_config,
        prepend_registry=False,
    )
    image_prefix_full = parse_docker_image_path(
        docker_config=build_base_docker_config,
        prepend_registry=True,
    )

    tags = [
        env.get('LANDSCAPE', str(time.time())),
    ]

    pip_install_str: str = get_pip_install_str(
        pip_install_packages=pip_packages,
    )

    # @formatter:off
    docker_file_str = textwrap.dedent(
        """
        # {auto_generated}
        # {dagster_url}
        FROM {parent_image} AS {image_name}
        LABEL authors="{AUTHOR}"

        {pip_install_str}

        WORKDIR {DAGSTER_ROOT}
        COPY ./payload/workspace.yaml .

        WORKDIR {DAGSTER_HOME}
        COPY ./payload/dagster.yaml .

        WORKDIR {DAGSTER_ROOT}

        ENTRYPOINT ["dagster", "dev"]
        CMD []
    """
    ).format(
        pip_install_str=pip_install_str.format(
            **env,
        ),
        auto_generated=f"AUTO-GENERATED by Dagster Asset {'__'.join(context.asset_key.path)}",
        dagster_url=urllib.parse.quote(
            f"http://localhost:3000/asset-groups/{'%2F'.join(context.asset_key.path)}",
            safe=":/%",
        ),
        image_name=image_name,
        # Todo: this won't work as expected if len(tags) > 1
        parent_image=f"{build_base_parent_image_prefix}{build_base_parent_image_name}:{build_base_parent_image_tags[0]}",
        **env,
    )
    # @formatter:on

    with open(docker_file, "w") as fw:
        fw.write(docker_file_str)

    payload = docker_file.parent / "payload"
    payload.mkdir(parents=True, exist_ok=True)

    # dagster.yaml
    if DAGSTER_USE_POSTGRES:
        dagster_yaml = pathlib.Path(
            env["CONFIGS_ROOT"],
            "materializations-postgres",
            "dagster.yaml",
        ).expanduser()
    else:
        dagster_yaml = pathlib.Path(
            env["CONFIGS_ROOT"],
            "materializations",
            "dagster.yaml",
        ).expanduser()

    # workspace.yaml
    shutil.copy(
        src=pathlib.Path(
            env["CONFIGS_ROOT"],
            "workspace.yaml",
        ).expanduser(),
        dst=payload,
    )

    # dagster.yaml
    shutil.copy(
        src=dagster_yaml,
        dst=payload,
    )

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    image_data = {
        "image_name": image_name,
        "image_prefix_local": image_prefix_local,
        "image_prefix_full": image_prefix_full,
        "image_tags": tags,
        "image_parent": copy.deepcopy(build_base_image_data),
    }

    context.log.debug(image_data)

    tags_list: list = docker_build(
        context=context,
        docker_config=build_base_docker_config,
        docker_file=docker_file,
        context_path=docker_file.parent,
        docker_use_cache=DOCKER_USE_CACHE,
        image_data=image_data,
    )

    yield Output(image_data)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(image_data),
            "tags_list": MetadataValue.json(tags_list),
            "docker_file": MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
            "env": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None]:

    compose_network_mode = ComposeNetworkMode.DEFAULT

    if compose_network_mode == ComposeNetworkMode.DEFAULT:
        docker_dict = {
            "networks": {
                "mongodb": {
                    "name": "network_mongodb-10-2",
                },
                "repository": {
                    "name": "network_repository-10-2",
                },
                "ayon": {
                    "name": "network_ayon-10-2",
                },
                "dagster": {
                    "name": "network_dagster",
                },
            },
        }

    else:
        docker_dict = {
            "network_mode": compose_network_mode.value,
        }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
        "build": AssetIn(
            AssetKey([*KEY, "build_docker_image"]),
        ),
    },
)
def compose_dagster(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    build: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    network_dict = {}
    ports_dict = {}
    depends_on_dict = {}

    if "networks" in compose_networks:
        network_dict = {
            "networks": list(compose_networks.get("networks", {}).keys())
        }
        ports_dict = {
            "ports": [
                f"{env.get('DAGSTER_DEV_PORT_HOST')}:{env.get('DAGSTER_DEV_PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {
            "network_mode": compose_networks.get("network_mode")
        }

    volumes_dict = {
        "volumes": [
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT')}",
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
        ]
    }

    if DAGSTER_USE_POSTGRES:

        depends_on_dict = {
            "depends_on": [
                env["POSTGRES_SERVICE_NAME"],
            ],
        }

    service_name = "dagster"
    container_name = service_name
    host_name = ".".join([service_name, env["ROOT_DOMAIN"]])

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname":  host_name,
                "domainname": env.get("ROOT_DOMAIN"),
                "restart": "always",
                "image": f"{build['image_prefix_full']}{build['image_name']}:{build['image_tags'][0]}",
                **copy.deepcopy(network_dict),
                "environment": {
                    "DAGSTER_HOME": env.get("DAGSTER_HOME"),
                    # Todo
                    #  - [ ] fix hard code here (from deadline-dagster .env)
                    "DAGSTER_DEPLOYMENT": "farm",
                    "DAGSTER_JOBS_IN": "/data/share/nfs/in",
                },
                "healthcheck": {
                    "test": [
                        "CMD",
                        "curl",
                        "-f",
                        f"http://localhost:{env.get('DAGSTER_DEV_PORT_CONTAINER')}",
                    ],
                    "interval": "10s",
                    "timeout": "2s",
                    "retries": "3",
                },
                "command": [
                    "--workspace",
                    env.get("DAGSTER_WORKSPACE"),
                    "--host",
                    env.get("DAGSTER_HOST"),
                    "--port",
                    env.get("DAGSTER_DEV_PORT_CONTAINER"),
                ],
                **copy.deepcopy(depends_on_dict),
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(ports_dict),
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
        # "build": AssetIn(
        #     AssetKey([*KEY, "build_docker_image"]),
        # ),
    },
)
def compose_postgres(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    # build: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    if not DAGSTER_USE_POSTGRES:

        ret = dict()

        yield Output(ret)

        yield AssetMaterialization(
            asset_key=context.asset_key,
            metadata={
                "__".join(context.asset_key.path): MetadataValue.json(ret),
            },
        )

    else:

        network_dict = {}
        ports_dict = {}

        if "networks" in compose_networks:
            network_dict = {
                "networks": list(compose_networks.get("networks", {}).keys())
            }
            ports_dict = {
                # "ports": [
                #     f"{env.get('POSTGRES_PORT_HOST')}:{env.get('POSTGRES_PORT_CONTAINER')}",
                # ]
            }
        elif "network_mode" in compose_networks:
            network_dict = {
                "network_mode": compose_networks.get("network_mode")
            }



        postgres_db_dir_host = (
            pathlib.Path(env.get("POSTGRES_DATABASE_INSTALL_DESTINATION"))
        )
        postgres_db_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {postgres_db_dir_host.as_posix()} created.")

        volumes_dict = {
            "volumes": [
                f"{postgres_db_dir_host.as_posix()}:{env.get('PGDATA')}",
                # f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
            ]
        }

        service_name = env["POSTGRES_SERVICE_NAME"]
        container_name = service_name
        host_name = ".".join([service_name, env["ROOT_DOMAIN"]])

        docker_dict = {
            "services": {
                service_name: {
                    "container_name": container_name,
                    "hostname":  host_name,
                    "domainname": env.get("ROOT_DOMAIN"),
                    "restart": "always",
                    "image": "docker.io/postgres",
                    **copy.deepcopy(network_dict),
                    "environment": {
                        "POSTGRES_USER": env.get("POSTGRES_USER"),
                        "POSTGRES_PASSWORD": env.get("POSTGRES_PASSWORD"),
                        "POSTGRES_DB": env.get("POSTGRES_DB"),
                        "PGDATA": env.get("PGDATA"),
                        # ??? "POSTGRES_PORT": env.get("PGDAPOSTGRES_PORT_CONTAINERTA"),
                    },
                    # Todo
                    #  "healthcheck": {
                    #      "test": [
                    #          "CMD",
                    #          "curl",
                    #          "-f",
                    #          f"http://localhost:{env.get('DAGSTER_DEV_PORT_CONTAINER')}",
                    #      ],
                    #      "interval": "10s",
                    #      "timeout": "2s",
                    #      "retries": "3",
                    #  },
                    # "command": [
                    #     "--workspace",
                    #     env.get("DAGSTER_WORKSPACE"),
                    #     "--host",
                    #     env.get("DAGSTER_HOST"),
                    #     "--port",
                    #     env.get("DAGSTER_DEV_PORT_CONTAINER"),
                    # ],
                    **copy.deepcopy(volumes_dict),
                    **copy.deepcopy(ports_dict),
                },
            },
        }

        docker_yaml = yaml.dump(docker_dict)

        yield Output(docker_dict)

        yield AssetMaterialization(
            asset_key=context.asset_key,
            metadata={
                "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
                "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
                # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
            },
        )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_dagster": AssetIn(
            AssetKey([*KEY, "compose_dagster"]),
        ),
        "compose_postgres": AssetIn(
            AssetKey([*KEY, "compose_postgres"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[list[dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


compose = AssetsDefinition.from_op(
    op_compose,
    tags_by_output_name={
        "compose": {
            "compose": "third_party",
        },
    },
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "compose_networks": AssetKey(
            [*KEY, "compose_networks"]
        ),
        "compose_maps": AssetKey(
            [*KEY, "compose_maps"]
        ),
    },
)


group_out = AssetsDefinition.from_op(
    op_group_out,
    can_subset=True,
    group_name=GROUP,
    tags_by_output_name={
        "group_out": {
            "group_out": "third_party",
        },
    },
    key_prefix=KEY,
    keys_by_input_name={
        "compose": AssetKey(
            [*KEY, "compose"]
        ),
        "env": AssetKey(
            [*KEY, "env"]
        ),
        "group_in": AssetKey(
            [*KEY_BASE, "group_out"]
        ),
    },
)


docker_compose_graph = AssetsDefinition.from_op(
    op_docker_compose_graph,
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "group_out": AssetKey(
            [*KEY, "group_out"]
        ),
        "compose_project_name": AssetKey(
            [*KEY, "compose_project_name"]
        ),
    },
)
