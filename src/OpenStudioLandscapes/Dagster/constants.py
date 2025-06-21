__all__ = [
    "DOCKER_USE_CACHE",
    "DAGSTER_USE_POSTGRES",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from pathlib import Path
from typing import Generator, Any

from dagster import (
    multi_asset,
    AssetOut,
    AssetMaterialization,
    AssetExecutionContext,
    Output,
    MetadataValue,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False


# Todo
#  - [ ] Integrate this into FEATURE_CONFIGS
DAGSTER_USE_POSTGRES = True


GROUP = "Dagster"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}".replace("_", "-")

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}

# @formatter:off
FEATURE_CONFIGS = {
    OpenStudioLandscapesConfig.DEFAULT: {
        "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
        "CONFIGS_ROOT": pathlib.Path(
            "{DOT_FEATURES}",
            FEATURE,
            ".payload",
            "config",
        )
        .expanduser()
        .as_posix(),
        "DAGSTER_DEV_PORT_HOST": "3003",
        "DAGSTER_DEV_PORT_CONTAINER": "3006",
        "DAGSTER_ROOT": "/dagster",
        "DAGSTER_HOME": "/dagster/materializations",
        "DAGSTER_HOST": "0.0.0.0",
        "DAGSTER_WORKSPACE": "/dagster/workspace.yaml",

        # Postgres
        # # If Dagster is used with MySQL (no Postgres)
        # # Uncomment everything below this (or create an
        # # extra OpenStudioLandscapesConfig)
        "POSTGRES_SERVICE_NAME": "openstudiolandscapes-postgres-dagster",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "mysecretpassword",
        "POSTGRES_DB": "postgres",
        "PGDATA": "/var/lib/postgresql/data/pgdata",
        "POSTGRES_PORT_HOST": "5432",
        "POSTGRES_PORT_CONTAINER": "5432",
        "POSTGRES_DATABASE_INSTALL_DESTINATION": {
            #################################################################
            #
            #################################################################
            #################################################################
            # Inside Landscape:
            "default": pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{LANDSCAPE}",
                f"{GROUP}__{'__'.join(KEY)}",
                "postgres",
            )
            .expanduser()
            .as_posix(),
            #################################################################
            # In Landscapes root dir:
            "landscapes_root": pathlib.Path(
                "{DOT_LANDSCAPES}",
                ".dagster",
                "postgres",
            )
            .expanduser()
            .as_posix(),
            # #################################################################
            # # Prod DB:
            # "prod_db": get
            #     pathlib.Path(
            #     "{NFS_ENTRY_POINT}",
            #     "services",
            #     "kitsu",
            # ).as_posix(),
            # #################################################################
            # # Test DB:
            # "test_db": pathlib.Path(
            #     "{NFS_ENTRY_POINT}",
            #     "test_data",
            #     "10.2",
            #     "kitsu",
            # ).as_posix(),
        }["landscapes_root"],
    }
}
# @formatter:on


# Todo:
#  - [ ] move to common_assets
@multi_asset(
    name=f"constants_{GROUP}",
    outs={
        "NAME": AssetOut(
            **ASSET_HEADER,
            dagster_type=str,
            description="",
        ),
        "FEATURE_CONFIGS": AssetOut(
            **ASSET_HEADER,
            dagster_type=dict,
            description="",
        ),
        "DOCKER_COMPOSE": AssetOut(
            **ASSET_HEADER,
            dagster_type=pathlib.Path,
            description="",
        ),
    },
)
def constants_multi_asset(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[OpenStudioLandscapesConfig, dict[str | Any, bool | str | Any]]] | AssetMaterialization | Output[Any] |
    Output[Path] | Any, None, None]:
    """ """

    yield Output(
        output_name="FEATURE_CONFIGS",
        value=FEATURE_CONFIGS,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("FEATURE_CONFIGS"),
        metadata={
            "__".join(
                context.asset_key_for_output("FEATURE_CONFIGS").path
            ): MetadataValue.json(FEATURE_CONFIGS),
        },
    )

    yield Output(
        output_name="NAME",
        value=__name__,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("NAME"),
        metadata={
            "__".join(
                context.asset_key_for_output("NAME").path
            ): MetadataValue.path(__name__),
        },
    )

    docker_compose = pathlib.Path(
        "{DOT_LANDSCAPES}",
        "{LANDSCAPE}",
        f"{ASSET_HEADER['group_name']}__{'_'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key_for_output("DOCKER_COMPOSE").path),
        "docker_compose",
        "docker-compose.yml",
    )

    yield Output(
        output_name="DOCKER_COMPOSE",
        value=docker_compose,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("DOCKER_COMPOSE"),
        metadata={
            "__".join(
                context.asset_key_for_output("DOCKER_COMPOSE").path
            ): MetadataValue.path(docker_compose),
        },
    )
