from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Dagster.assets
from OpenStudioLandscapes.Dagster import (
    dist,
    LOGGER,
)

LOGGER.info(f"Loading {dist.name} assets...")

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Dagster.assets],
)


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
