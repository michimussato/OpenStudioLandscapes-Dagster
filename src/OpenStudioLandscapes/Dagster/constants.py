__all__ = [
    "DOCKER_USE_CACHE",
    "DAGSTER_USE_POSTGRES",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "ENVIRONMENT",
    "COMPOSE_SCOPE",
]

import pathlib
from typing import Generator, MutableMapping

from dagster import (
    AssetExecutionContext,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL, THIRD_PARTY
from OpenStudioLandscapes.engine.exceptions import ComposeScopeException
from OpenStudioLandscapes.engine.utils import *

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False


DAGSTER_USE_POSTGRES = True


GROUP = "Dagster"
KEY = [GROUP]

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
    "compute_kind": "python",
}

# @formatter:off
ENVIRONMENT = {
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
}
# @formatter:on

# @formatter:off
_env_postgres = {
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
# @formatter:on
if DAGSTER_USE_POSTGRES:
    ENVIRONMENT.update(_env_postgres)

# Todo
#  - [ ] This is a bit hacky
_module = __name__
_parent = ".".join(_module.split(".")[:-1])
_definitions = ".".join([_parent, "definitions"])

COMPOSE_SCOPE = None
for i in THIRD_PARTY:
    if i["module"] == _definitions:
        COMPOSE_SCOPE = i["compose_scope"]
        break

if COMPOSE_SCOPE is None:
    raise ComposeScopeException(
        "No compose_scope found for module '%s'. Is the module enabled "
        "in `OpenStudioLandscapes.engine.constants.THIRD_PARTY`?" % _module
    )


@asset(
    **ASSET_HEADER,
    description="",
)
def constants(
    context: AssetExecutionContext,
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    _constants = dict()

    _constants["DOCKER_USE_CACHE"] = DOCKER_USE_CACHE
    _constants["ASSET_HEADER"] = ASSET_HEADER
    _constants["ENVIRONMENT"] = ENVIRONMENT

    yield Output(_constants)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_constants),
        },
    )
