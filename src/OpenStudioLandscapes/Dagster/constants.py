__all__ = [
    "DOCKER_USE_CACHE",
    "DAGSTER_USE_POSTGRES",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from typing import Generator, MutableMapping

from dagster import (
    multi_asset,
    AssetOut,
    AssetMaterialization,
    AssetExecutionContext,
    Output,
    MetadataValue,
    AssetsDefinition,
    AssetKey,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.base.ops import op_constants
from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False


# Todo
#  - [ ] Integrate this into FEATURE_CONFIGS
DAGSTER_USE_POSTGRES = True


GROUP = "Dagster"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}"

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}

# @formatter:off
FEATURE_CONFIGS = {
    OpenStudioLandscapesConfig.DEFAULT: {
        "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
        "CONFIGS_ROOT": pathlib.Path(
            get_configs_root(pathlib.Path(__file__)),
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


constants = AssetsDefinition.from_op(
    op_constants,
    can_subset=False,
    group_name=GROUP,
    keys_by_input_name={
        "group_in": AssetKey([*ASSET_HEADER["key_prefix"], "group_in"]),
        "NAME": AssetKey([*ASSET_HEADER["key_prefix"], "NAME"]),
    },
    keys_by_output_name={
        "COMPOSE_SCOPE": AssetKey([*ASSET_HEADER["key_prefix"], "COMPOSE_SCOPE"]),
        "FEATURE_CONFIG": AssetKey([*ASSET_HEADER["key_prefix"], "FEATURE_CONFIG"]),
        # "FEATURE_CONFIGS": AssetKey([*ASSET_HEADER["key_prefix"], "FEATURE_CONFIGS"]),
        # "DOCKER_USE_CACHE": AssetKey([*ASSET_HEADER["key_prefix"], "DOCKER_USE_CACHE"]),
    }
)


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
    },
)
def constants_multi_asset(
    context: AssetExecutionContext,
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
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
