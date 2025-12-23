[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Dagster](#feature-openstudiolandscapes-dagster)
   1. [Brief](#brief)
   2. [Configuration](#configuration)
2. [External Resources](#external-resources)
   1. [Official Documentation (Version 1.9)](#official-documentation-version-19)
   2. [Getting Started with Dagster](#getting-started-with-dagster)
   3. [Resources](#resources)
3. [Community](#community)
4. [Technical Reference](#technical-reference)
   1. [Requirements](#requirements)
   2. [Install](#install)
      1. [This Feature](#this-feature)
   3. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Dagster

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Configuration

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

> [!TIP]
> 
> To specify a config store location different than
> the default, you can do so be setting the environment variable
> `OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT`:
> 
> ```shell
> OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT="~/.config/OpenStudioLandscapes/my-custom-config-store"
> ```

The following settings are available in `OpenStudioLandscapes-Dagster` and are accessible throughout the [`OpenStudioLandscapes-Dagster`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/OpenStudioLandscapes/Dagster/config/models.py) package.

```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class:
#     Description:
#         None
#     Default value:
#         None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class:
#     Description:
#         None
#     Default value:
#         None


# =============
# config_parent
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.FeatureBaseModel'>
# Base Class:
#     Description:
#         None
#     Default value:
#         None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class:
#     Description:
#         None
#     Default value:
#         None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class:
#     Description:
#         None
#     Default value:
#         None


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class:
#     Description:
#         None
#     Default value:
#         None


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class:
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class:
#     Description:
#         None
#     Default value:
#         default


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class:
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
feature_name: OpenStudioLandscapes-Dagster


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class:
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml


# =====================
# dagster_dev_port_host
# ---------------------
#
# Type: <class 'int'>
# Sub Class Description:
#     The Dagster UI container port.
# Examples:
#     None
dagster_dev_port_host: 3003


# ==========================
# dagster_dev_port_container
# --------------------------
#
# Type: <class 'int'>
# Sub Class Description:
#     The Dagster UI container port.
# Examples:
#     None
dagster_dev_port_container: 3006


# ============
# dagster_root
# ------------
#
# Type: <class 'pathlib.Path'>
# Sub Class Description:
#     The container side Dagster root directory.
# Examples:
#     None
dagster_root: /dagster


# ============
# dagster_home
# ------------
#
# Type: <class 'pathlib.Path'>
# Sub Class Description:
#     The container side Dagster HOME directory.
# Examples:
#     None
dagster_home: /dagster/materializations


# ===================
# dagster_listen_addr
# -------------------
#
# Type: <class 'str'>
# Sub Class Description:
#     The listen address.
# Examples:
#     None
dagster_listen_addr: 0.0.0.0


# ============================================
# dagster_enable_openstudiolandscapes_showcase
# --------------------------------------------
#
# Type: <class 'bool'>
# Sub Class Description:
#     Enable the OpenStudioLandscapes Dagster Showcase project (https://github.com/michimussato/OpenStudioLandscapes-Dagster-Showcase).
# Examples:
#     None
dagster_enable_openstudiolandscapes_showcase: true


# =============================
# dagster_postgres_service_name
# -----------------------------
#
# Type: <class 'str'>
# Sub Class Description:
#     Dagster postgres Docker service name.
# Examples:
#     None
dagster_postgres_service_name: openstudiolandscapes-postgres-dagster


# =======================
# dagster_enable_postgres
# -----------------------
#
# Type: <class 'bool'>
# Sub Class Description:
#     Enable Postgres for Dagster.
# Examples:
#     None
dagster_enable_postgres: true


# ======================
# dagster_postgres_image
# ----------------------
#
# Type: <class 'str'>
# Sub Class Description:
#     Dagster postgres Docker image.
# Examples:
#     None
dagster_postgres_image: docker.io/postgres:17


# =====================
# dagster_postgres_user
# ---------------------
#
# Type: <class 'str'>
# Sub Class Description:
#     Dagster postgres user.
# Examples:
#     None
dagster_postgres_user: postgres


# =========================
# dagster_postgres_password
# -------------------------
#
# Type: <class 'str'>
# Sub Class Description:
#     Dagster postgres password.
# Examples:
#     None
dagster_postgres_password: mysecretpassword


# ===================
# dagster_postgres_db
# -------------------
#
# Type: <class 'str'>
# Sub Class Description:
#     Dagster postgres database name.
# Examples:
#     None
dagster_postgres_db: postgres


# =======================
# dagster_postgres_pgdata
# -----------------------
#
# Type: <class 'pathlib.Path'>
# Sub Class Description:
#     Dagster postgres PGDATA directory.
# Examples:
#     None
dagster_postgres_pgdata: /var/lib/postgresql/data/pgdata


# ==========================
# dagster_postgres_port_host
# --------------------------
#
# Type: <class 'int'>
# Sub Class Description:
#     The Dagster postgres container port.
# Examples:
#     None
dagster_postgres_port_host: 5432


# ===============================
# dagster_postgres_port_container
# -------------------------------
#
# Type: <class 'int'>
# Sub Class Description:
#     The Dagster postgres host port.
# Examples:
#     None
dagster_postgres_port_container: 5432


# ===============================
# dagster_postgres_db_install_dir
# -------------------------------
#
# Type: <class 'pathlib.Path'>
# Sub Class Description:
#     Dagster host side postgres database directory.
# Examples:
#     None
dagster_postgres_db_install_dir: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/postgres'



```

***

# External Resources

[![Logo Dagster ](https://dagster-website.vercel.app/images/brand/logos/dagster-primary-horizontal.png)](https://dagster.io/platform)

Dagster is written and maintained by Dagster Labs.

[![Logo Dagster Labs ](https://docs.dagster.io/img/dagster_labs-primary-horizontal.svg)](https://dagster.io)

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

***

# Community

| Feature                              | GitHub                                                                                                                                       | Discord                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| OpenStudioLandscapes                 | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                 | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)         |
| OpenStudioLandscapes-Ayon            | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                       | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)            |
| OpenStudioLandscapes-Dagster         | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                 | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)         |
| OpenStudioLandscapes-Flamenco        | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)               | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)        |
| OpenStudioLandscapes-Flamenco-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker) | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p) |
| OpenStudioLandscapes-Kitsu           | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                     | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)           |
| OpenStudioLandscapes-RustDeskServer  | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)   | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)  |
| OpenStudioLandscapes-Template        | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)               | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)        |
| OpenStudioLandscapes-VERT            | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                       | [# openstudiolandscapes-twingate](https://discord.gg/FYaFRUwbYr)        |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

# Technical Reference

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

***

Last changed: **2025-12-23 12:26:13 UTC**