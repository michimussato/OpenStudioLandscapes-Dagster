[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Dagster](#feature-openstudiolandscapes-dagster)
   1. [Brief](#brief)
   2. [Install](#install)
   3. [Configure](#configure)
      1. [Default Configuration](#default-configuration)
2. [External Resources](#external-resources)
   1. [Official Documentation (Version 1.9)](#official-documentation-version-19)
   2. [Getting Started with Dagster](#getting-started-with-dagster)
   3. [Resources](#resources)
3. [Community](#community)

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

## Install

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes install-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Dagster.git
# Check the resulting console output for installation instructions

```

For more info on `pip` see [VCS Support of `pip`](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Configure

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

> [!TIP]
> 
> To specify a config store location different from
> the default location, check out the OpenStudioLandscapes 
> [CLI Section](https://github.com/michimussato/OpenStudioLandscapes#cli)
> to find out how to do that.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

The following settings are available in `OpenStudioLandscapes-Dagster` and are based on [`OpenStudioLandscapes-Dagster/tree/main/OpenStudioLandscapes/Dagster/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/OpenStudioLandscapes/Dagster/config/models.py).

### Default Configuration


<details>
<summary><code>config.yml</code></summary>


```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_parent
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.FeatureBaseModel'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Group name. This will represent the group node name. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
group_name: OpenStudioLandscapes_Dagster


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Asset key prefixes. This will be reflected in the nesting (directory structure) of the Asset. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
key_prefixes:
- OpenStudioLandscapes_Dagster


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True
# Description:
#     Whether the Feature is enabled or not.
# Required:
#     False
# Examples:
#     None


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         default
# Description:
#     None
# Required:
#     False
# Examples:
#     ['default', 'license_server', 'worker']


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
feature_name: OpenStudioLandscapes-Dagster


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml
# Description:
#     The path to the `docker-compose.yml` file.
# Required:
#     False
# Examples:
#     None


# =====================
# dagster_dev_port_host
# ---------------------
#
# Type: <class 'int'>
# Description:
#     The Dagster UI container port.
# Required:
#     False
# Examples:
#     None
dagster_dev_port_host: 3003


# ==========================
# dagster_dev_port_container
# --------------------------
#
# Type: <class 'int'>
# Description:
#     The Dagster UI container port.
# Required:
#     False
# Examples:
#     None
dagster_dev_port_container: 3006


# ============
# dagster_root
# ------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The container side Dagster root directory.
# Required:
#     False
# Examples:
#     None
dagster_root: /dagster


# ============
# dagster_home
# ------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The container side Dagster HOME directory.
# Required:
#     False
# Examples:
#     None
dagster_home: /dagster/materializations


# ===================
# dagster_listen_addr
# -------------------
#
# Type: <class 'str'>
# Description:
#     The listen address.
# Required:
#     False
# Examples:
#     None
dagster_listen_addr: 0.0.0.0


# =============================
# dagster_postgres_service_name
# -----------------------------
#
# Type: <class 'str'>
# Description:
#     Dagster postgres Docker service name.
# Required:
#     False
# Examples:
#     None
dagster_postgres_service_name: openstudiolandscapes-postgres-dagster


# =======================
# dagster_enable_postgres
# -----------------------
#
# Type: <class 'bool'>
# Description:
#     Enable Postgres for Dagster.
# Required:
#     False
# Examples:
#     None
dagster_enable_postgres: true


# ======================
# dagster_postgres_image
# ----------------------
#
# Type: <class 'str'>
# Description:
#     Dagster postgres Docker image.
# Required:
#     False
# Examples:
#     None
dagster_postgres_image: docker.io/postgres:17


# =====================
# dagster_postgres_user
# ---------------------
#
# Type: <class 'str'>
# Description:
#     Dagster postgres user.
# Required:
#     False
# Examples:
#     None
dagster_postgres_user: postgres


# =========================
# dagster_postgres_password
# -------------------------
#
# Type: <class 'str'>
# Description:
#     Dagster postgres password.
# Required:
#     False
# Examples:
#     None
dagster_postgres_password: mysecretpassword


# ===================
# dagster_postgres_db
# -------------------
#
# Type: <class 'str'>
# Description:
#     Dagster postgres database name.
# Required:
#     False
# Examples:
#     None
dagster_postgres_db: postgres


# =======================
# dagster_postgres_pgdata
# -----------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Dagster postgres PGDATA directory.
# Required:
#     False
# Examples:
#     None
dagster_postgres_pgdata: /var/lib/postgresql/data/pgdata


# ==========================
# dagster_postgres_port_host
# --------------------------
#
# Type: <class 'int'>
# Description:
#     The Dagster postgres container port.
# Required:
#     False
# Examples:
#     None
dagster_postgres_port_host: 5432


# ===============================
# dagster_postgres_port_container
# -------------------------------
#
# Type: <class 'int'>
# Description:
#     The Dagster postgres host port.
# Required:
#     False
# Examples:
#     None
dagster_postgres_port_container: 5432


# ===============================
# dagster_postgres_db_install_dir
# -------------------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Dagster host side postgres database directory.
# Required:
#     False
# Examples:
#     None
dagster_postgres_db_install_dir: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/postgres'


# ============
# apt_packages
# ------------
#
# Type: typing.List
# Description:
#     None
# Required:
#     False
# Examples:
#     None
apt_packages:
- sqlite3


# ============
# pip_packages
# ------------
#
# Type: typing.List
# Description:
#     None
# Required:
#     False
# Examples:
#     None
pip_packages:
- dagster==1.9.11
- dagster-webserver==1.9.11
- dagster-postgres==0.25.11


# ======================
# dagster_code_locations
# ----------------------
#
# Type: typing.Dict[str, typing.List[typing.Dict]]
# Description:
#     The Dagster code locations. If nothing is specified, the default value should be `load_from: []`.
# Required:
#     False
# Examples:
#     None
dagster_code_locations:
  load_from:
  - python_module:
      location_name: OpenStudioLandscapes-Dagster-Showcase Package Code Location
      module_name: OpenStudioLandscapes.Dagster.Showcase.definitions
      pip_path: OpenStudioLandscapes-Dagster-Showcase @ git+https://github.com/michimussato/OpenStudioLandscapes-Dagster-Showcase.git@main
      working_directory: src
```


</details>


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

| Feature                                   | GitHub                                                                                                                                                 | Discord                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| OpenStudioLandscapes                      | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                           | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)              |
| OpenStudioLandscapes-Ayon                 | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                 | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)                 |
| OpenStudioLandscapes-Dagster              | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                           | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)              |
| OpenStudioLandscapes-Deadline-10-2        | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)               | [# openstudiolandscapes-deadline-10-2](https://discord.gg/p2UjxHk4Y3)        |
| OpenStudioLandscapes-Deadline-10-2-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker) | [# openstudiolandscapes-deadline-10-2-worker](https://discord.gg/ttkbfkzUmf) |
| OpenStudioLandscapes-Flamenco             | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)                         | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)             |
| OpenStudioLandscapes-Flamenco-Worker      | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker)           | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p)      |
| OpenStudioLandscapes-Grafana              | [https://github.com/michimussato/OpenStudioLandscapes-Grafana](https://github.com/michimussato/OpenStudioLandscapes-Grafana)                           | [# openstudiolandscapes-grafana](https://discord.gg/gEDQ8vJWDb)              |
| OpenStudioLandscapes-Kitsu                | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                               | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)                |
| OpenStudioLandscapes-LikeC4               | [https://github.com/michimussato/OpenStudioLandscapes-LikeC4](https://github.com/michimussato/OpenStudioLandscapes-LikeC4)                             | [# openstudiolandscapes-likec4](https://discord.gg/qAYYsKYF6V)               |
| OpenStudioLandscapes-OpenCue              | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue](https://github.com/michimussato/OpenStudioLandscapes-OpenCue)                           | [# openstudiolandscapes-opencue](https://discord.gg/3DdCZKkVyZ)              |
| OpenStudioLandscapes-OpenCue-Worker       | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker](https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker)             | [# openstudiolandscapes-opencue-worker](https://discord.gg/n9fxxhHa3V)       |
| OpenStudioLandscapes-RustDeskServer       | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)             | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)       |
| OpenStudioLandscapes-Syncthing            | [https://github.com/michimussato/OpenStudioLandscapes-Syncthing](https://github.com/michimussato/OpenStudioLandscapes-Syncthing)                       | [# openstudiolandscapes-syncthing](https://discord.gg/upb9MCqb3X)            |
| OpenStudioLandscapes-Template             | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)                         | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)             |
| OpenStudioLandscapes-VERT                 | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                                 | [# openstudiolandscapes-vert](https://discord.gg/EPrX5fzBCf)                 |
| OpenStudioLandscapes-filebrowser          | [https://github.com/michimussato/OpenStudioLandscapes-filebrowser](https://github.com/michimussato/OpenStudioLandscapes-filebrowser)                   | [# openstudiolandscapes-filebrowser](https://discord.gg/stzNsZBmwk)          |
| OpenStudioLandscapes-n8n                  | [https://github.com/michimussato/OpenStudioLandscapes-n8n](https://github.com/michimussato/OpenStudioLandscapes-n8n)                                   | [# openstudiolandscapes-n8n](https://discord.gg/yFYrG999wE)                  |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

Last changed: **2026-01-25 17:55:01 UTC**