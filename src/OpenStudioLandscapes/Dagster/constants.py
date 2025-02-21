__all__ = [
    "DOCKER_USE_CACHE",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "ENVIRONMENT",
]


DOCKER_USE_CACHE = False


GROUP = "Dagster"
KEY = GROUP

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": [KEY],
    "compute_kind": "python",
}

# @formatter:off
ENVIRONMENT = {
    "DAGSTER_DEV_PORT_HOST": "3003",
    "DAGSTER_DEV_PORT_CONTAINER": "3006",
    "DAGSTER_ROOT": "/dagster",
    "DAGSTER_HOME": "/dagster/materializations",
    "DAGSTER_HOST": "0.0.0.0",
    "DAGSTER_WORKSPACE": "/dagster/workspace.yaml",
}
# @formatter:on
