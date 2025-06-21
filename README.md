[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Dagster](#feature-openstudiolandscapes-dagster)
   1. [Brief](#brief)
   2. [Requirements](#requirements)
   3. [Install](#install)
      1. [This Feature](#this-feature)
   4. [Add to OpenStudioLandscapes](#add-to-openstudiolandscapes)
   5. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)
   6. [Variables](#variables)
      1. [Feature Configs](#feature-configs)
2. [Community](#community)
3. [Official Resources](#official-resources)
   1. [Official Documentation (Version 1.9)](#official-documentation-version-19)
   2. [Getting Started with Dagster](#getting-started-with-dagster)
   3. [Resources](#resources)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Dagster

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

You feel like writing your own Feature? Go and check out the [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Requirements

- `python-3.11`
- `OpenStudioLandscapes`

## Install

### This Feature

Clone this repository into `OpenStudioLandscapes/.features`:

```shell

# cd .features
git clone https://github.com/michimussato/OpenStudioLandscapes-Dagster.git

```

Create `venv`:

```shell

# cd .features/OpenStudioLandscapes-Dagster
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools

```

Configure `venv`:

```shell

# cd .features/OpenStudioLandscapes-Dagster
pip install -e "../../[dev]"
pip install -e ".[dev]"

```

For more info see [VCS Support of pip](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Add to OpenStudioLandscapes

Add the following code to `OpenStudioLandscapes.engine.features.FEATURES`:

```python

FEATURES.update(
    "OpenStudioLandscapes-Dagster": {
        "enabled": True|False,
        # - from ENVIRONMENT VARIABLE (.env):
        #   "enabled": get_bool_env("ENV_VAR")
        # - combined:
        #   "enabled": True|False or get_bool_env(
        #       "OPENSTUDIOLANDSCAPES__ENABLE_FEATURE_OPENSTUDIOLANDSCAPES_DAGSTER"
        #   )
        "module": "OpenStudioLandscapes.Dagster.definitions",
        "compose_scope": ComposeScope.DEFAULT,
        "feature_config": OpenStudioLandscapesConfig.DEFAULT,
    }
)

```

## Testing

### pre-commit

- https://pre-commit.com
- https://pre-commit.com/hooks.html

```shell

pre-commit install

```

### nox

#### Generate Report

```shell

nox --no-error-on-missing-interpreters --report .nox/nox-report.json

```

#### Re-Generate this README

```shell

nox -v --add-timestamp --session readme

```

#### Generate Sphinx Documentation

```shell

nox -v --add-timestamp --session docs

```

#### pylint

```shell

nox -v --add-timestamp --session lint

```

##### pylint: disable=redefined-outer-name

- [`W0621`](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html): Due to Dagsters way of piping arguments into assets.

#### SBOM

Acronym for Software Bill of Materials

```shell

nox -v --add-timestamp --session sbom

```

We create the following SBOMs:

- [`cyclonedx-bom`](https://pypi.org/project/cyclonedx-bom/)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Dot)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Mermaid)

SBOMs for the different Python interpreters defined in [`.noxfile.VERSIONS`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/noxfile.py) will be created in the [`.sbom`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/.sbom) directory of this repository.

- `cyclone-dx`
- `pipdeptree` (Dot)
- `pipdeptree` (Mermaid)

Currently, the following Python interpreters are enabled for testing:

- `python3.11`
- `python3.12`

## Variables

The following variables are being declared in `OpenStudioLandscapes.Dagster.constants` and are accessible throughout the [`OpenStudioLandscapes-Dagster`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/constants.py) package.

| Variable               | Type   |
| :--------------------- | :----- |
| `DOCKER_USE_CACHE`     | `bool` |
| `DAGSTER_USE_POSTGRES` | `bool` |
| `ASSET_HEADER`         | `dict` |
| `FEATURE_CONFIGS`      | `dict` |

### Feature Configs

#### Feature Config: default

| Variable                                | Type   | Value                                                         |
| :-------------------------------------- | :----- | :------------------------------------------------------------ |
| `DOCKER_USE_CACHE`                      | `bool` | `False`                                                       |
| `CONFIGS_ROOT`                          | `str`  | `{DOT_FEATURES}/OpenStudioLandscapes-Dagster/.payload/config` |
| `DAGSTER_DEV_PORT_HOST`                 | `str`  | `3003`                                                        |
| `DAGSTER_DEV_PORT_CONTAINER`            | `str`  | `3006`                                                        |
| `DAGSTER_ROOT`                          | `str`  | `/dagster`                                                    |
| `DAGSTER_HOME`                          | `str`  | `/dagster/materializations`                                   |
| `DAGSTER_HOST`                          | `str`  | `0.0.0.0`                                                     |
| `DAGSTER_WORKSPACE`                     | `str`  | `/dagster/workspace.yaml`                                     |
| `POSTGRES_SERVICE_NAME`                 | `str`  | `openstudiolandscapes-postgres-dagster`                       |
| `POSTGRES_USER`                         | `str`  | `postgres`                                                    |
| `POSTGRES_PASSWORD`                     | `str`  | `mysecretpassword`                                            |
| `POSTGRES_DB`                           | `str`  | `postgres`                                                    |
| `PGDATA`                                | `str`  | `/var/lib/postgresql/data/pgdata`                             |
| `POSTGRES_PORT_HOST`                    | `str`  | `5432`                                                        |
| `POSTGRES_PORT_CONTAINER`               | `str`  | `5432`                                                        |
| `POSTGRES_DATABASE_INSTALL_DESTINATION` | `str`  | `{DOT_LANDSCAPES}/.dagster/postgres`                          |

# Community

| Feature                      | GitHub                                                                                                                       | Discord                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| OpenStudioLandscapes         | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                 | [# openstudiolandscapes-general](https://discord.com/channels/1357343453364748419/1357343454065328202) |
| OpenStudioLandscapes-Ayon    | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)       | [# openstudiolandscapes-ayon](https://discord.com/channels/1357343453364748419/1357722468336271411)    |
| OpenStudioLandscapes-Dagster | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster) | [# openstudiolandscapes-dagster](https://discord.com/channels/1357343453364748419/1358016764608249856) |
| OpenStudioLandscapes-Kitsu   | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)     | [# openstudiolandscapes-kitsu](https://discord.com/channels/1357343453364748419/1357638253632688231)   |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

# Official Resources

[![ Logo Dagster ](https://dagster-website.vercel.app/images/brand/logos/dagster-primary-horizontal.png)](https://dagster.io/platform)

Dagster is written and maintained by Dagster Labs.

[![ Logo Dagster Labs ](https://docs.dagster.io/img/dagster_labs-primary-horizontal.svg)](https://dagster.io)

Dagster is available in two flavors:

1. [Dagster Community](https://dagster.io/community)
2. [Dagster+](https://dagster.io/plus)

`OpenStudioLandscapes-Dagster` is based on the Community release. Dagster is evolving at a very fast pace and it can be hard to keep up. Therefore, for now, the Dagster version used in `OpenStudioLandscapes-Dagster` is locked to [version 1.9.11](https://pypi.org/project/dagster/1.9.11/). When consulting the official [Dagster Documentation](https://docs.dagster.io), make sure you consult the matching [version](#official-documentation-version-19).

## Official Documentation (Version 1.9)

- [https://release-1-9-13.archive.dagster-docs.io](https://release-1-9-13.archive.dagster-docs.io)

## Getting Started with Dagster

Dagsters primary learning resource is called [Dagster University](https://courses.dagster.io). It is a fantastic learning path and you should check it out if you plan to use Dagster as you automation platform (a personal recommendation by the `OpenStudioLandscapes-Dagster` maintainer). The course [Dagster Essentials](https://courses.dagster.io/courses/dagster-essentials) will give you a basic but deep enough understanding of how Dagster works.

## Resources

- [All Resources](https://dagster.io/resources)
- [GitHub](https://github.com/dagster-io/dagster)
- [Issue Tracker](https://github.com/dagster-io/dagster/issues)
- [PyPi](https://pypi.org/project/dagster)
- [Slack](https://app.slack.com/client/TCDGQDUKF)