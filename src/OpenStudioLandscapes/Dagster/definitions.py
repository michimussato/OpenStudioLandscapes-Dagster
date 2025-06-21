from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Dagster.assets
import OpenStudioLandscapes.Dagster.constants

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Dagster.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Dagster.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
