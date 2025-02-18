from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Dagster.assets


assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Dagster.assets],
)


defs = Definitions(
    assets=[
        *assets,
    ],
)
