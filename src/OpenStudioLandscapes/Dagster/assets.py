import copy
import json
import pathlib
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
)

from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker import *

from OpenStudioLandscapes.Dagster.constants import *

from OpenStudioLandscapes.engine.common_assets.constants import get_constants
from OpenStudioLandscapes.engine.common_assets.docker_config import get_docker_config
from OpenStudioLandscapes.engine.common_assets.env import get_env
from OpenStudioLandscapes.engine.common_assets.group_in import get_group_in
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import get_docker_compose_graph
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.docker_config_json import get_docker_config_json


# Todo:
#  - [ ] Create dagster.yaml dynamically


constants = get_constants(
    ASSET_HEADER=ASSET_HEADER,
)


docker_config = get_docker_config(
    ASSET_HEADER=ASSET_HEADER,
)


group_in = get_group_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_PARENT=ASSET_HEADER_BASE,
    input_name=str(GroupIn.BASE_IN),
)


env = get_env(
    ASSET_HEADER=ASSET_HEADER,
)


group_out = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out = get_feature_out(
    ASSET_HEADER=ASSET_HEADER,
    feature_out_ins={
        "env": dict,
        "compose": dict,
        "group_in": dict,
    },
)


docker_config_json = get_docker_config_json(
    ASSET_HEADER=ASSET_HEADER,
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
        "dagster==1.9.11",
        "dagster-webserver==1.9.11",
        # "dagster-shared[dev] @ git+https://github.com/michimussato/dagster-shared.git@main",
        # "dagster-job-processor[dev] @ git+https://github.com/michimussato/dagster-job-processor.git@main",
        "OpenStudioLandscapes-Dagster-Showcase[dev] @ git+https://github.com/michimussato/OpenStudioLandscapes-Dagster-Showcase.git@main",
    ]

    if DAGSTER_USE_POSTGRES:
        _pip_packages.extend(
            [
                "dagster-postgres==0.25.11",
            ]
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
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "docker_config_json": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "docker_config_json"]),
        ),
        "group_in": AssetIn(AssetKey([*ASSET_HEADER_BASE["key_prefix"], str(GroupIn.BASE_IN)])),
        "pip_packages": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "pip_packages"]),
        ),
    },
)
def build_docker_image(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    docker_config_json: pathlib.Path,  # pylint: disable=redefined-outer-name
    group_in: dict,  # pylint: disable=redefined-outer-name
    pip_packages: list,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    build_base_image_data: dict = group_in["docker_image"]
    build_base_docker_config: DockerConfig = group_in["docker_config"]

    if build_base_docker_config.value["docker_push"]:
        build_base_parent_image_prefix: str = build_base_image_data["image_prefix_full"]
    else:
        build_base_parent_image_prefix: str = build_base_image_data[
            "image_prefix_local"
        ]

    build_base_parent_image_name: str = build_base_image_data["image_name"]
    build_base_parent_image_tags: list = build_base_image_data["image_tags"]

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
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
        env.get("LANDSCAPE", str(time.time())),
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

        RUN mkdir -p {DAGSTER_ROOT}
        RUN mkdir -p {DAGSTER_HOME}

        WORKDIR {DAGSTER_ROOT}

        ENTRYPOINT []
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

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    image_data = {
        "image_name": image_name,
        "image_prefix_local": image_prefix_local,
        "image_prefix_full": image_prefix_full,
        "image_tags": tags,
        "image_parent": copy.deepcopy(build_base_image_data),
    }

    context.log.info(f"{image_data = }")

    cmds = []

    tags_local = [f"{image_prefix_local}{image_name}:{tag}" for tag in tags]
    tags_full = [f"{image_prefix_full}{image_name}:{tag}" for tag in tags]

    cmd_build = docker_build_cmd(
        context=context,
        docker_config_json=docker_config_json,
        docker_file=docker_file,
        tags_local=tags_local,
        tags_full=tags_full,
    )

    cmds.append(cmd_build)

    cmds_push = docker_push_cmd(
        context=context,
        docker_config_json=docker_config_json,
        tags_full=tags_full,
    )

    cmds.extend(cmds_push)

    context.log.info(f"{cmds = }")

    logs = []

    for logs_ in docker_process_cmds(
        context=context,
        cmds=cmds,
    ):
        logs.append(logs_)

    yield Output(image_data)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(image_data),
            "docker_file": MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
            "env": MetadataValue.json(env),
            "logs": MetadataValue.json(logs),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
    },
    description="Visit https://docs.dagster.io/guides/deploy/dagster-yaml for reference. "
    "For more info regarding Postgres backend for Dagster, visit "
    "https://docs.dagster.io/api/python-api/libraries/dagster-postgres and "
    "https://docs.dagster.io/guides/deploy/dagster-instance-configuration.",
)
def dagster_yaml(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    # @formatter:off

    concurrency_dict = {}
    storage_dict = {}

    if DAGSTER_USE_POSTGRES:
        # dagster.yaml with Postgres backend
        """
        Reference

        # https://docs.dagster.io/guides/deploy/dagster-yaml
        ## https://docs.dagster.io/guides/limiting-concurrency-in-data-pipelines
        run_queue:
          max_concurrent_runs: 1
          block_op_concurrency_limited_runs:
            enabled: true
        #concurrency:
        #  default_op_concurrency_limit: 1
        telemetry:
          enabled: false
        #run_monitoring:
        #  enabled: true
        #  free_slots_after_run_end_seconds: 300
        auto_materialize:
          enabled: true
          use_sensors: true
        storage:
          postgres:
            postgres_db:
              username: postgres
              password: mysecretpassword
        #      hostname: openstudiolandscapes-postgres-dagster.farm.evil
              hostname: openstudiolandscapes-postgres-dagster
              db_name: postgres
              port: 5432
        """

        storage_dict = {
            "storage": {
                "postgres": {
                    "postgres_db": {
                        "username": str(env.get("POSTGRES_USER")),
                        "password": str(env.get("POSTGRES_PASSWORD")),
                        "hostname": ".".join(
                            [
                                str(env.get("POSTGRES_SERVICE_NAME")),
                                env["ROOT_DOMAIN"],
                            ],
                        ),
                        "db_name": str(env.get("POSTGRES_DB")),
                        "port": int(env.get("POSTGRES_PORT_CONTAINER")),
                    }
                }
            }
        }
    else:
        # dagster.yaml with default MySQL backend
        """
        Reference

        # https://docs.dagster.io/guides/deploy/dagster-yaml
        ## https://docs.dagster.io/guides/limiting-concurrency-in-data-pipelines
        run_queue:
          max_concurrent_runs: 1
          block_op_concurrency_limited_runs:
            enabled: true
        concurrency:
          default_op_concurrency_limit: 1
        telemetry:
          enabled: false
        #run_monitoring:
        #  enabled: true
        #  free_slots_after_run_end_seconds: 300
        auto_materialize:
          enabled: true
          use_sensors: true
        """

        concurrency_dict = {"concurrency": {"default_op_concurrency_limit": 1}}

    dagster_yaml_dict = {
        "run_queue": {
            "max_concurrent_runs": 1,
            "block_op_concurrency_limited_runs": {
                "enabled": True,
            },
        },
        "telemetry": {
            "enabled": False,
        },
        "auto_materialize": {
            "enabled": True,
            "use_sensors": True,
        },
        **concurrency_dict,
        **storage_dict,
    }

    dagster_yaml_load = yaml.dump(dagster_yaml_dict)

    dagster_yaml_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key.path),
        "materializations",
        "dagster.yaml",
    ).expanduser()

    dagster_yaml_file.parent.mkdir(parents=True, exist_ok=True)

    with open(dagster_yaml_file, "w") as fw:
        fw.write(dagster_yaml_load)

    yield Output(dagster_yaml_file)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(dagster_yaml_file),
            "use_postgres": MetadataValue.bool(DAGSTER_USE_POSTGRES),
            "dagster_yaml_dict": MetadataValue.json(dagster_yaml_dict),
            "dagster_yaml": MetadataValue.md(f"```\n{dagster_yaml_load}\n```"),
            "env": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
    },
    description="Visit https://docs.dagster.io/guides/deploy/code-locations/workspace-yaml for reference.",
)
def workspace_yaml(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    # @formatter:off

    """
    Reference

    load_from:
    #  - python_package:
    #      package_name: My-Skeleton-Package
    #      location_name: "My Skeleton Package Location"
    # Todo:
    #  - [ ] dynamic workspace.yaml to be able to add dagster-shared dynamically (https://github.com/michimussato/dagster-shared)
    #  - [ ] Shouldn't this be OpenStudioLandscapes.open_studio_landscapes also?
      - python_module:
          # https://github.com/michimussato/deadline-dagster
          working_directory: src
          module_name: OpenStudioLandscapes.dagster_job_processor.definitions
          location_name: "dagster_job_processor Package Location"
          # executable_path: ../.venv/bin/python
    #  - python_module:
    #      # Todo:
    #      #  - [ ] will only work after making studio-landscapes public
    #      # https://github.com/michimussato/deadline-dagster
    #      working_directory: src
    #      module_name: OpenStudioLandscapes.open_studio_landscapes.definitions
    #      location_name: "OpenStudioLandscapes.open_studio_landscapes Package Location"
    #      # executable_path: ../.venv/bin/python
    """

    workspace_yaml_dict = {
        "load_from": [
            {
                "python_module": {
                    "working_directory": "src",
                    "module_name": "OpenStudioLandscapes.dagster_job_processor.definitions",
                    "location_name": "dagster_job_processor Package Code Location",
                },
            },
            {
                "python_module": {
                    "working_directory": "src",
                    "module_name": "openstudiolandscapes_dagster_showcase.definitions",
                    "location_name": "openstudiolandscapes_dagster_showcase Package Code Location",
                },
            }
        ],
    }

    workspace_yaml_load = yaml.dump(workspace_yaml_dict)

    workspace_yaml_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key.path),
        "workspace.yaml",
    ).expanduser()

    workspace_yaml_file.parent.mkdir(parents=True, exist_ok=True)

    with open(workspace_yaml_file, "w") as fw:
        fw.write(workspace_yaml_load)

    yield Output(workspace_yaml_file)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(workspace_yaml_file),
            "use_postgres": MetadataValue.bool(DAGSTER_USE_POSTGRES),
            "workspace_yaml_dict": MetadataValue.json(workspace_yaml_dict),
            "workspace_yaml": MetadataValue.md(f"```\n{workspace_yaml_load}\n```"),
            "env": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None
]:

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
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "dagster_yaml": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "dagster_yaml"]),
        ),
        "workspace_yaml": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "workspace_yaml"]),
        ),
    },
)
def compose_dagster(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    build: dict,  # pylint: disable=redefined-outer-name
    dagster_yaml: pathlib.Path,  # pylint: disable=redefined-outer-name
    workspace_yaml: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    network_dict = {}
    ports_dict = {}
    depends_on_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{env.get('DAGSTER_DEV_PORT_HOST')}:{env.get('DAGSTER_DEV_PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks.get("network_mode")}

    # ./materializations
    # with ./materlializations/dagster.yaml inside
    materializations_dagster_yaml_container = pathlib.Path(
        env.get("DAGSTER_HOME"),
    )
    workspace_yaml_container = pathlib.Path(env.get("DAGSTER_ROOT"), "workspace.yaml")

    volumes_dict = {
        "volumes": [
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT')}",
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
            f"{dagster_yaml.parent.as_posix()}:{materializations_dagster_yaml_container.as_posix()}:rw",
            f"{workspace_yaml.as_posix()}:{workspace_yaml_container.as_posix()}:ro",
        ]
    }

    if DAGSTER_USE_POSTGRES:

        depends_on_dict = {
            "depends_on": [
                env["POSTGRES_SERVICE_NAME"],
            ],
        }

    service_name = "dagster"
    container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    host_name = ".".join([service_name, env["ROOT_DOMAIN"]])

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
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
                    "dagster",
                    "dev",
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
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
    },
    description="See https://docs.dagster.io/guides/deploy/deployment-options/docker and "
    "https://docs.dagster.io/api/python-api/libraries/dagster-postgres.",
)
def compose_postgres(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
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
            network_dict = {"network_mode": compose_networks.get("network_mode")}

        postgres_db_dir_host = pathlib.Path(
            env.get("POSTGRES_DATABASE_INSTALL_DESTINATION")
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
        container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
        host_name = ".".join([service_name, env["ROOT_DOMAIN"]])

        docker_dict = {
            "services": {
                service_name: {
                    "container_name": container_name,
                    "hostname": host_name,
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
                    "healthcheck": {
                        "test": [
                            "CMD-SHELL",
                            f"pg_isready --username {env.get('POSTGRES_USER')} --dbname {env.get('POSTGRES_DB')} --port {env.get('POSTGRES_PORT_CONTAINER')}",
                        ],
                        "interval": "10s",
                        "timeout": "8s",
                        "retries": "5",
                    },
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
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_dagster"]),
        ),
        "compose_postgres": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_postgres"]),
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
