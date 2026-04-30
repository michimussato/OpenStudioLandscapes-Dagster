import pathlib
from typing import Dict, List

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

from OpenStudioLandscapes.cli import LOGGING_LEVEL_DEFAULT

LOGGER = get_dagster_logger(__name__)
LOGGER.setLevel(LOGGING_LEVEL_DEFAULT)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.Dagster import constants, dist


class Config(FeatureBaseModel):
    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    dagster_dev_port_host: PositiveInt = Field(
        default=3003,  # Must not clash with the local OpenStudioLandscapes Dagster instance (default=3000).
        description="The Dagster UI container port.",
        frozen=True,
    )

    dagster_dev_port_container: PositiveInt = Field(
        default=3006,
        description="The Dagster UI container port.",
        frozen=True,
    )

    dagster_root: pathlib.Path = Field(
        description="The container side Dagster root directory.",
        default=pathlib.Path("/dagster"),
    )

    dagster_home: pathlib.Path = Field(
        description="The container side Dagster HOME directory.",
        default=pathlib.Path("/dagster/materializations"),
    )

    dagster_listen_addr: str = Field(
        description="The listen address.",
        default="0.0.0.0",
    )

    dagster_postgres_service_name: str = Field(
        description="Dagster postgres Docker service name.",
        default="openstudiolandscapes-postgres-dagster",
    )

    dagster_enable_postgres: bool = Field(
        description="Enable Postgres for Dagster.",
        default=True,
    )

    dagster_postgres_image: str = Field(
        description="Dagster postgres Docker image.",
        default="docker.io/postgres:17",
    )

    dagster_postgres_user: str = Field(
        description="Dagster postgres user.",
        default="postgres",
    )

    dagster_postgres_password: str = Field(
        description="Dagster postgres password.",
        default="mysecretpassword",
    )

    dagster_postgres_db: str = Field(
        description="Dagster postgres database name.",
        default="postgres",
    )

    dagster_postgres_pgdata: pathlib.Path = Field(
        description="Dagster postgres PGDATA directory.",
        default=pathlib.Path("/var/lib/postgresql/data/pgdata"),
    )

    dagster_postgres_port_host: PositiveInt = Field(
        default=5432,
        description="The Dagster postgres container port.",
        frozen=True,
    )

    dagster_postgres_port_container: PositiveInt = Field(
        default=5432,
        description="The Dagster postgres host port.",
        frozen=True,
    )

    dagster_postgres_db_install_dir: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/postgres"),
        description="Dagster host side postgres database directory.",
    )

    apt_packages: List = Field(
        default=[
            "sqlite3",
        ],
        frozen=True,
    )

    pip_packages: List = Field(
        default=[
            "dagster==1.9.11",
            "dagster-webserver==1.9.11",
            # Needed if dagster_enable_postgres is True
            "dagster-postgres==0.25.11",
            # OpenStudioLandscapes-Dagster Showcase package:
            # "OpenStudioLandscapes-DagsterCodeLocation-Showcase @ git+https://github.com/michimussato/OpenStudioLandscapes-DagsterCodeLocation-Showcase.git@main",
        ],
        frozen=True,
    )

    dagster_code_locations: Dict[str, List[Dict]] = Field(
        default={
            "load_from": [
                {
                    "python_module": {
                        "location_name": "OpenStudioLandscapes-DagsterCodeLocation-Showcase Package Code Location",
                        "module_name": "OpenStudioLandscapes.DagsterCodeLocation.Showcase.definitions",
                        "working_directory": "src",
                        "pip_path": "OpenStudioLandscapes-DagsterCodeLocation-Showcase @ git+https://github.com/michimussato/OpenStudioLandscapes-DagsterCodeLocation-Showcase.git@main",
                        # "volume_mounts": [],
                        # "environment": {},
                    }
                }
            ],
        },
        description="The Dagster code locations. If nothing is specified, the default value should be `load_from: []`.",
    )

    # EXPANDABLE PATHS
    @property
    def dagster_postgres_db_install_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.dagster_postgres_db_install_dir}...")
        ret = pathlib.Path(
            self.dagster_postgres_db_install_dir.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


if __name__ == "__main__":
    CONFIG_STR = Config.get_docs()
else:
    import yaml
    CONFIG_STR = yaml.dump(
        Config.model_json_schema(mode="serialization"),
    )
