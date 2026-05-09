[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Dagster](#feature-openstudiolandscapes-dagster)
   1. [Brief](#brief)
   2. [Clone](#clone)
      1. [Clone and Install](#clone-and-install)
   3. [Configure](#configure)
      1. [Default Configuration](#default-configuration)
   4. [Local Development/Unit Testing/Debugging](#local-developmentunit-testingdebugging)
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

## Clone

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Dagster.git
deactivate
# Check the resulting console output for installation instructions
```

### Clone and Install

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Dagster.git \
    && pip install --editable ./.features/OpenStudioLandscapes-Dagster
deactivate
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

The following settings are available in `OpenStudioLandscapes-Dagster` and are based on [`OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/config/models.py).

### Default Configuration

<details open>
<summary><code>config.yml</code></summary>


```yaml
properties:
  apt_packages:
    default:
    - sqlite3
    items: {}
    title: Apt Packages
    type: array
  compose_scope:
    default: default
    examples:
    - default
    - license_server
    - worker
    title: Compose Scope
    type: string
  dagster_code_locations:
    additionalProperties:
      items:
        additionalProperties: true
        type: object
      type: array
    default:
      load_from:
      - python_module:
          location_name: OpenStudioLandscapes-DagsterCodeLocation-Showcase Package
            Code Location
          module_name: OpenStudioLandscapes.DagsterCodeLocation.Showcase.definitions
          pip_path: OpenStudioLandscapes-DagsterCodeLocation-Showcase @ git+https://github.com/michimussato/OpenStudioLandscapes-DagsterCodeLocation-Showcase.git@main
          working_directory: src
    description: 'The Dagster code locations. If nothing is specified, the default
      value should be `load_from: []`.'
    title: Dagster Code Locations
    type: object
  dagster_dev_port_container:
    default: 3006
    description: The Dagster UI container port.
    exclusiveMinimum: 0
    title: Dagster Dev Port Container
    type: integer
  dagster_dev_port_host:
    default: 3003
    description: The Dagster UI container port.
    exclusiveMinimum: 0
    title: Dagster Dev Port Host
    type: integer
  dagster_enable_postgres:
    default: true
    description: Enable Postgres for Dagster.
    title: Dagster Enable Postgres
    type: boolean
  dagster_home:
    default: /dagster/materializations
    description: The container side Dagster HOME directory.
    format: path
    title: Dagster Home
    type: string
  dagster_listen_addr:
    default: 0.0.0.0
    description: The listen address.
    title: Dagster Listen Addr
    type: string
  dagster_postgres_db:
    default: postgres
    description: Dagster postgres database name.
    title: Dagster Postgres Db
    type: string
  dagster_postgres_db_install_dir:
    default: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/postgres'
    description: Dagster host side postgres database directory.
    format: path
    title: Dagster Postgres Db Install Dir
    type: string
  dagster_postgres_image:
    default: docker.io/postgres:17
    description: Dagster postgres Docker image.
    title: Dagster Postgres Image
    type: string
  dagster_postgres_password:
    default: mysecretpassword
    description: Dagster postgres password.
    title: Dagster Postgres Password
    type: string
  dagster_postgres_pgdata:
    default: /var/lib/postgresql/data/pgdata
    description: Dagster postgres PGDATA directory.
    format: path
    title: Dagster Postgres Pgdata
    type: string
  dagster_postgres_port_container:
    default: 5432
    description: The Dagster postgres host port.
    exclusiveMinimum: 0
    title: Dagster Postgres Port Container
    type: integer
  dagster_postgres_port_host:
    default: 5432
    description: The Dagster postgres container port.
    exclusiveMinimum: 0
    title: Dagster Postgres Port Host
    type: integer
  dagster_postgres_service_name:
    default: openstudiolandscapes-postgres-dagster
    description: Dagster postgres Docker service name.
    title: Dagster Postgres Service Name
    type: string
  dagster_postgres_user:
    default: postgres
    description: Dagster postgres user.
    title: Dagster Postgres User
    type: string
  dagster_root:
    default: /dagster
    description: The container side Dagster root directory.
    format: path
    title: Dagster Root
    type: string
  docker_compose:
    default: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml'
    description: The path to the `docker-compose.yml` file.
    format: path
    title: Docker Compose
    type: string
  enabled:
    default: true
    description: Whether the Feature is enabled or not.
    title: Enabled
    type: boolean
  env:
    additionalProperties: true
    title: Env
    type: object
  feature_name:
    default: OpenStudioLandscapes-Dagster
    title: Feature Name
    type: string
  group_name:
    default: OpenStudioLandscapes_Dagster
    title: Group Name
    type: string
  key_prefixes:
    default:
    - OpenStudioLandscapes_Dagster
    items:
      type: string
    title: Key Prefixes
    type: array
  local_bind_volumes:
    description: Here you can define Feature specific, arbitrary, absolute bind volume
      mappings.
    items:
      type: string
    title: Local Bind Volumes
    type: array
  local_environment_variables:
    additionalProperties:
      type: string
    description: Here you can define Feature specific, arbitrary environment variables.
    title: Local Environment Variables
    type: object
  pip_packages:
    default:
    - dagster==1.9.11
    - dagster-webserver==1.9.11
    - dagster-postgres==0.25.11
    items: {}
    title: Pip Packages
    type: array
title: Config
type: object

```

</details>


## Local Development/Unit Testing/Debugging

This is for isolated development, unit testing and debugging. Instead of the [`OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/definitions.py`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/definitions.py), the accompanying [`OpenStudioLandscapes-Dagster/tree/main/workspace.yaml`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/workspace.yaml) loads the [`OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/_definitions_with_upstream_specs.py`](https://github.com/michimussato/OpenStudioLandscapes-Dagster/tree/main/src/OpenStudioLandscapes/Dagster/_definitions_with_upstream_specs.py) which also contains [`AssetSpec`](https://release-1-9-13.archive.dagster-docs.io/api/dagster/assets#dagster.AssetSpec) definitions for upstream dependencies as [external assets](https://release-1-9-13.archive.dagster-docs.io/guides/build/assets/external-assets).

```shell
# cd ./.features/OpenStudioLandscapes-Dagster
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools setuptools_scm wheel
pip install --editable .[dev]
dagster dev --workspace workspace.yaml
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

Last changed: **2026-05-09 11:21:26 UTC**