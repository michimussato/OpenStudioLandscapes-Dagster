<!-- TOC -->
* [OpenStudioLandscapes-Dagster](#openstudiolandscapes-dagster)
<!-- TOC -->

---

# OpenStudioLandscapes-Dagster

This is for isolated development, unit testing and debugging.
Instead of the [`definitions.py`](src/OpenStudioLandscapes/Dagster/definitions.py), 
the accompanying [`workspace.yaml`](workspace.yaml) loads 
the [`_definitions_with_upstream_specs.py`](src/OpenStudioLandscapes/Dagster/_definitions_with_upstream_specs.py) 
which also contains 
[`AssetSpec`](https://release-1-9-13.archive.dagster-docs.io/api/dagster/assets#dagster.AssetSpec)
definitions for upstream dependencies as 
[external assets](https://release-1-9-13.archive.dagster-docs.io/guides/build/assets/external-assets).

```shell
dagster dev --workspace workspace.yaml
```
