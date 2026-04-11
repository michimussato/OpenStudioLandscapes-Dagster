from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Dagster.assets

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Dagster.assets],
)


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
