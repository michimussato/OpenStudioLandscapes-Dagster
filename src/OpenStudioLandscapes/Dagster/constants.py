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
    AssetExecutionContext,
    AssetMaterialization,
    MetadataValue,
    Output,
    AssetOut,
    AssetIn,
    AssetKey,
    multi_asset,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig, ComposeScope
from OpenStudioLandscapes.engine.base.assets import KEY_BASE

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


@multi_asset(
    name=f"constants_{GROUP}",
    ins={"group_in": AssetIn(AssetKey([*KEY_BASE, "group_out"]))},
    outs={
        "COMPOSE_SCOPE": AssetOut(
            **ASSET_HEADER,
            dagster_type=ComposeScope,
            description="",
        ),
        "FEATURE_CONFIG": AssetOut(
            **ASSET_HEADER,
            dagster_type=OpenStudioLandscapesConfig,
            description="",
        ),
        "FEATURE_CONFIGS": AssetOut(
            **ASSET_HEADER,
            dagster_type=dict,
            description="",
        ),
        "DOCKER_USE_CACHE": AssetOut(
            **ASSET_HEADER,
            dagster_type=bool,
            description="",
        ),
    },
)
def constants(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    features = group_in["features"]

    # COMPOSE_SCOPE
    COMPOSE_SCOPE = get_compose_scope(
        context=context,
        features=features,
        name=__name__,
    )

    # FEATURE_CONFIG
    FEATURE_CONFIG = get_feature_config(
        context=context,
        features=features,
        name=__name__,
    )

    yield Output(
        output_name="COMPOSE_SCOPE",
        value=COMPOSE_SCOPE,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("COMPOSE_SCOPE"),
        metadata={
            "__".join(
                context.asset_key_for_output("COMPOSE_SCOPE").path
            ): MetadataValue.json(COMPOSE_SCOPE),
        },
    )

    yield Output(
        output_name="FEATURE_CONFIG",
        value=FEATURE_CONFIG,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("FEATURE_CONFIG"),
        metadata={
            "__".join(
                context.asset_key_for_output("FEATURE_CONFIG").path
            ): MetadataValue.json(FEATURE_CONFIG),
        },
    )

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
        output_name="DOCKER_USE_CACHE",
        value=DOCKER_USE_CACHE,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("DOCKER_USE_CACHE"),
        metadata={
            "__".join(
                context.asset_key_for_output("DOCKER_USE_CACHE").path
            ): MetadataValue.bool(DOCKER_USE_CACHE),
        },
    )
