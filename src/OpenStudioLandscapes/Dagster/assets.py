import copy
import enum
import pathlib
import textwrap
import urllib.parse
from typing import Dict, Generator, List, Union

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    AssetsDefinition,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.common_assets.cmd import get_feature__cmd
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.feature import get_feature__CONFIG
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out_v2
from OpenStudioLandscapes.engine.common_assets.group_in import (
    get_feature_in,
    get_feature_in_parent,
)
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.config.models import ConfigEngine, DockerConfigModel
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.link.models import OpenStudioLandscapesFeatureIn
from OpenStudioLandscapes.engine.policies.retry import build_docker_image_retry_policy
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import *

from OpenStudioLandscapes.Dagster import dist
from OpenStudioLandscapes.Dagster.config.models import CONFIG_STR, Config
from OpenStudioLandscapes.Dagster.constants import *

# Todo:
#  - [ ] Create dagster.yaml dynamically

# https://github.com/yaml/pyyaml/issues/722#issuecomment-1969292770
yaml.SafeDumper.add_multi_representer(
    data_type=enum.Enum,
    representer=yaml.representer.SafeRepresenter.represent_str,
)


cmd: AssetsDefinition = get_feature__cmd(
    ASSET_HEADER=ASSET_HEADER,
)

CONFIG: AssetsDefinition = get_feature__CONFIG(
    ASSET_HEADER=ASSET_HEADER,
    CONFIG_STR=CONFIG_STR,
    search_model_of_type=Config,
)


feature_in: AssetsDefinition = get_feature_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_BASE=ASSET_HEADER_BASE,
    ASSET_HEADER_FEATURE_IN={},
)


group_out: AssetsDefinition = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph: AssetsDefinition = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose: AssetsDefinition = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out_v2: AssetsDefinition = get_feature_out_v2(
    ASSET_HEADER=ASSET_HEADER,
)


# Produces
# - feature_in_parent
# - CONFIG_PARENT
# if ConfigParent is or type FeatureBaseModel
feature_in_parent: Union[AssetsDefinition, None] = get_feature_in_parent(
    ASSET_HEADER=ASSET_HEADER,
    config_parent=ConfigParent,
)


@asset(
    **ASSET_HEADER,
    ins={
        "feature_in": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "feature_in"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def write_dockerfile(
    context: AssetExecutionContext,
    feature_in: OpenStudioLandscapesFeatureIn,  # pylint: disable=redefined-outer-name
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    docker_config: DockerConfigModel = config_engine.openstudiolandscapes__docker_config

    docker_image: Dict = feature_in.openstudiolandscapes_base.docker_image_base
    context.log.debug(f"{docker_image = }")
    # docker_image = {'image_name': 'openstudiolandscapes_base_build_docker_image', 'image_prefixes': '', 'image_tags': ['2025-11-17-01-26-31-05a9b85aa33b47ffa7dfb21a28ca24ab'], 'image_parent': {}}

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    docker_file.parent.mkdir(parents=True, exist_ok=True)

    #################################################

    (
        image_name,
        image_prefixes,
        tags,
        build_base_parent_image_prefix,
        build_base_parent_image_name,
        build_base_parent_image_tags,
    ) = get_image_metadata(
        context=context,
        docker_image=docker_image,
        docker_config=docker_config,
        env=env,
    )

    #################################################

    apt_install_str: str = get_apt_install_str(
        apt_install_packages=CONFIG.apt_packages,
    )

    pip_install_str: str = get_pip_install_str(
        pip_install_packages=[
            *CONFIG.pip_packages,
            *[
                python_module.get("python_module", {"pip_path": ""})["pip_path"]
                for python_module in CONFIG.dagster_code_locations.get("load_from", [])
            ],
        ],
        bust_cache=True,
    )

    # @formatter:off
    docker_file_str = textwrap.dedent("""\
        # {auto_generated}
        # {dagster_url}
        FROM {parent_image} AS {image_name}
        LABEL authors="{AUTHOR}"

        {apt_install_str}

        {pip_install_str}

        RUN mkdir -p {dagster_root}
        RUN mkdir -p {dagster_home}

        WORKDIR {dagster_root}

        ENTRYPOINT []
        CMD []
        """).format(
        apt_install_str=apt_install_str,
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
        dagster_root=CONFIG.dagster_root,
        dagster_home=CONFIG.dagster_home,
        **env,
    )
    # @formatter:on

    with open(docker_file, "w") as fw:
        fw.write(docker_file_str)

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    yield Output(docker_file)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(docker_file),
            docker_file.name: MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "feature_in": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "feature_in"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "write_dockerfile": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "write_dockerfile"])
        ),
    },
    retry_policy=build_docker_image_retry_policy,
)
def build_docker_image(
    context: AssetExecutionContext,
    feature_in: OpenStudioLandscapesFeatureIn,  # pylint: disable=redefined-outer-name
    CONFIG: Config,  # pylint: disable=redefined-outer-name
    write_dockerfile: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    docker_config_json: pathlib.Path = (
        feature_in.openstudiolandscapes_base.docker_config_json
    )

    config_engine: ConfigEngine = CONFIG.config_engine

    docker_config: DockerConfigModel = config_engine.openstudiolandscapes__docker_config

    docker_image: Dict = feature_in.openstudiolandscapes_base.docker_image_base
    context.log.debug(f"{docker_image = }")

    (
        image_name,
        image_prefixes,
        tags,
        build_base_parent_image_prefix,
        build_base_parent_image_name,
        build_base_parent_image_tags,
    ) = get_image_metadata(
        context=context,
        docker_image=docker_image,
        docker_config=docker_config,
        env=env,
    )

    #################################################

    image_data, logs = create_image(
        context=context,
        image_name=image_name,
        image_prefixes=image_prefixes,
        tags=tags,
        docker_image=docker_image,
        docker_config=docker_config,
        docker_config_json=docker_config_json,
        docker_file=write_dockerfile,
    )

    yield Output(image_data)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(image_data),
            "env": MetadataValue.json(env),
            "docker_image": MetadataValue.path(
                f"{image_data['image_prefixes']}{image_data['image_name']}:{image_data['image_tags'][0]}"
            ),
            "docker_cmd": MetadataValue.path(
                get_docker_run_cmd(
                    context=context,
                    image_data=image_data,
                )
            ),
            "logs": MetadataValue.json(logs),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description=textwrap.dedent("""
        Visit https://docs.dagster.io/guides/deploy/dagster-yaml for reference.
        "For more info regarding Postgres backend for Dagster, visit
        "https://docs.dagster.io/api/python-api/libraries/dagster-postgres and
        "https://docs.dagster.io/guides/deploy/dagster-instance-configuration.
        
        ---
        
        # Reference
        
        ## MySQL Backend
        
        ```yaml
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
        ```
        
        ## Postgres Backend
        
        ```yaml
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
              hostname: openstudiolandscapes-postgres-dagster
              db_name: postgres
              port: 5432
        ```
        """),
)
def dagster_yaml(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:

    config_engine: ConfigEngine = CONFIG.config_engine

    env: Dict = CONFIG.env

    concurrency_dict = {}
    storage_dict = {}

    if CONFIG.dagster_enable_postgres:
        # dagster.yaml with Postgres backend
        storage_dict = {
            "storage": {
                "postgres": {
                    "postgres_db": {
                        "username": CONFIG.dagster_postgres_user,
                        "password": CONFIG.dagster_postgres_password,
                        "hostname": ".".join(
                            [
                                CONFIG.dagster_postgres_service_name,
                                config_engine.openstudiolandscapes__domain_lan,
                            ],
                        ),
                        "db_name": CONFIG.dagster_postgres_db,
                        "port": CONFIG.dagster_postgres_port_container,
                    }
                }
            }
        }
    else:
        # dagster.yaml with default MySQL backend
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
        f"{dist.name}",
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
            "use_postgres": MetadataValue.bool(CONFIG.dagster_enable_postgres),
            "dagster_yaml": MetadataValue.md(f"```yaml\n{dagster_yaml_load}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description=textwrap.dedent("""
        Visit https://docs.dagster.io/guides/deploy/code-locations/workspace-yaml for reference.
        
        ---
        
        # Reference
        
        ```yaml
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
        ```
        """),
)
def workspace_yaml(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:

    env: Dict = CONFIG.env

    """
    # Reference workspace.yaml:
    load_from:
    - python_module:
        location_name: OpenStudioLandscapes-Dagster-Showcase Package Code Location
        module_name: OpenStudioLandscapes.Dagster.Showcase.definitions
        working_directory: src
    - python_module:
        location_name: OpenStudioLandscapes-Dagster-JobProcessor Package Code Location
        module_name: OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.definitions
        working_directory: src
    """

    workspace_yaml_dict = copy.deepcopy(CONFIG.dagster_code_locations)

    for code_location in workspace_yaml_dict["load_from"]:

        pip_path = code_location["python_module"].pop("pip_path")
        # volume_mounts = code_location["python_module"].pop("volume_mounts")
        # environment = code_location["python_module"].pop("environment")

    workspace_yaml_load = yaml.dump(workspace_yaml_dict)

    workspace_yaml_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
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
            "use_postgres": MetadataValue.bool(CONFIG.dagster_enable_postgres),
            "workspace_yaml": MetadataValue.md(f"```yaml\n{workspace_yaml_load}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def compose_networks(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[Dict[str, Dict[str, Dict[str, str]]]] | AssetMaterialization, None, None
]:

    env: Dict = CONFIG.env

    compose_network_mode = DockerComposePolicies.NETWORK_MODE.BRIDGE

    docker_dict = get_network_dicts(
        context=context,
        compose_network_mode=compose_network_mode,
        env=env,
    )

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
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
    CONFIG: Config,  # pylint: disable=redefined-outer-name
    compose_networks: Dict,  # pylint: disable=redefined-outer-name
    build: Dict,  # pylint: disable=redefined-outer-name
    dagster_yaml: pathlib.Path,  # pylint: disable=redefined-outer-name
    workspace_yaml: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    network_dict = {}
    ports_dict = {}
    depends_on_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{CONFIG.dagster_dev_port_host}:{CONFIG.dagster_dev_port_container}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks["network_mode"]}

    # ./materializations
    # with ./materlializations/dagster.yaml inside
    materializations_dagster_yaml_container = pathlib.Path(
        CONFIG.dagster_home,
    )
    workspace_yaml_container = pathlib.Path(CONFIG.dagster_root, "workspace.yaml")

    volumes_dict = {
        "volumes": [
            f"{dagster_yaml.parent.as_posix()}:{materializations_dagster_yaml_container.as_posix()}:rw",
            f"{workspace_yaml.as_posix()}:{workspace_yaml_container.as_posix()}:ro",
        ]
    }

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

        host, container = v.split(":", maxsplit=1)

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=CONFIG.docker_compose_expanded,
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    # volume_mounts = []
    # env_ = {}
    #
    # for python_module in CONFIG.dagster_code_locations.get("load_from", []):
    #     # for volume in volume_mount["python_module"]["volume_mounts"]:
    #     volume_mounts.extend(python_module["python_module"].get("volume_mounts", []))
    #     env_.update(python_module["python_module"].get("environment", {}))

    volumes_dict = {
        "volumes": list(
            {
                *_volume_relative,
                *config_engine.global_bind_volumes,
                *CONFIG.local_bind_volumes,
            }
        )
    }

    if CONFIG.dagster_enable_postgres:

        depends_on_dict = {
            "depends_on": [
                CONFIG.dagster_postgres_service_name,
            ],
        }

    service_name = "dagster"
    container_name, host_name = get_docker_compose_names(
        context=context,
        service_name=service_name,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                # "image": "${DOT_OVERRIDES_REGISTRY_NAMESPACE:-docker.io/openstudiolandscapes}/%s:%s"
                # % (build["image_name"], build["image_tags"][0]),
                "image": "%s%s:%s"
                % (
                    build["image_prefixes"],
                    build["image_name"],
                    build["image_tags"][0],
                ),
                **copy.deepcopy(network_dict),
                "environment": {
                    "TZ": config_engine.tz,
                    "DAGSTER_HOME": CONFIG.dagster_home.as_posix(),
                    **config_engine.global_environment_variables,
                    **CONFIG.local_environment_variables,
                },
                "healthcheck": {
                    "test": [
                        "CMD",
                        "curl",
                        "-f",
                        f"http://localhost:{CONFIG.dagster_dev_port_container}",
                    ],
                    "interval": "10s",
                    "timeout": "2s",
                    "retries": "3",
                },
                "command": [
                    "dagster",
                    "dev",
                    "--workspace",
                    workspace_yaml_container.as_posix(),
                    "--host",
                    CONFIG.dagster_listen_addr,
                    "--port",
                    str(CONFIG.dagster_dev_port_container),
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
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
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
    CONFIG: Config,  # pylint: disable=redefined-outer-name
    compose_networks: Dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    if not CONFIG.dagster_enable_postgres:

        ret: Dict = {}

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
                #     f"{env['POSTGRES_PORT_HOST']}:{env['POSTGRES_PORT_CONTAINER']}",
                # ]
            }
        elif "network_mode" in compose_networks:
            network_dict = {"network_mode": compose_networks["network_mode"]}

        postgres_db_dir_host: pathlib.Path = (
            CONFIG.dagster_postgres_db_install_dir_expanded
        )
        postgres_db_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {postgres_db_dir_host.as_posix()} created.")

        # Is:
        # - "/home/michael/git/repos/OpenStudioLandscapes/.landscapes/.dagster/postgres:/var/lib/postgresql/data/pgdata"
        #
        # Want:
        # - ../../../../.dagster/postgres:/var/lib/postgresql/data/pgdata
        #
        # Get:
        # - ../../../../.dagster/postgres:/var/lib/postgresql/data/pgdata

        # For portability, convert absolute volume paths to relative paths
        volumes_paths_to_convert = [
            f"{postgres_db_dir_host.as_posix()}:{CONFIG.dagster_postgres_pgdata}",
        ]

        _volume_relative = []

        for v in volumes_paths_to_convert:

            host, container = v.split(":", maxsplit=1)

            volume_dir_host_rel_path = get_relative_path_via_common_root(
                context=context,
                path_src=CONFIG.docker_compose_expanded,
                path_dst=pathlib.Path(host),
                path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
            )

            _volume_relative.append(
                f"{volume_dir_host_rel_path.as_posix()}:{container}",
            )

        volumes_dict = {
            "volumes": list(
                {
                    *_volume_relative,
                    *config_engine.global_bind_volumes,
                    *CONFIG.local_bind_volumes,
                }
            )
        }

        service_name = CONFIG.dagster_postgres_service_name
        container_name, host_name = get_docker_compose_names(
            context=context,
            service_name=service_name,
            landscape_id=env.get("LANDSCAPE", "default"),
            domain_lan=config_engine.openstudiolandscapes__domain_lan,
        )

        docker_dict = {
            "services": {
                service_name: {
                    "container_name": container_name,
                    "hostname": host_name,
                    "domainname": config_engine.openstudiolandscapes__domain_lan,
                    "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                    "image": CONFIG.dagster_postgres_image,
                    **copy.deepcopy(network_dict),
                    "environment": {
                        "TZ": config_engine.tz,
                        "POSTGRES_USER": CONFIG.dagster_postgres_user,
                        "POSTGRES_PASSWORD": CONFIG.dagster_postgres_password,
                        "POSTGRES_DB": CONFIG.dagster_postgres_db,
                        "PGDATA": CONFIG.dagster_postgres_pgdata.as_posix(),
                        # ??? "POSTGRES_PORT": env.get("PGDAPOSTGRES_PORT_CONTAINERTA"),
                        **config_engine.global_environment_variables,
                        **CONFIG.local_environment_variables,
                    },
                    "healthcheck": {
                        "test": [
                            "CMD-SHELL",
                            f"pg_isready --username {CONFIG.dagster_postgres_user} --dbname {CONFIG.dagster_postgres_db} --port {str(CONFIG.dagster_postgres_port_container)}",
                        ],
                        "interval": "10s",
                        "timeout": "8s",
                        "retries": "5",
                    },
                    # "command": [
                    #     "--workspace",
                    #     env["DAGSTER_WORKSPACE"],
                    #     "--host",
                    #     env["DAGSTER_HOST"],
                    #     "--port",
                    #     env["DAGSTER_DEV_PORT_CONTAINER"],
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
                "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
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
) -> Generator[Output[List[Dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
