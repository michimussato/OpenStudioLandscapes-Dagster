import pathlib

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.str_gen import get_config_str
from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.Dagster import dist


class Config(FeatureBaseModel):
    feature_name: str = dist.name

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

    dagster_enable_openstudiolandscapes_showcase: bool = Field(
        description="Enable the OpenStudioLandscapes Dagster Showcase "
        "project (https://github.com/michimussato/OpenStudioLandscapes-Dagster-Showcase).",
        default=True,
    )

    # Todo
    # dagster_enable_openstudiolandscapes_shared: bool = Field(
    #     description="Enable the OpenStudioLandscapes Dagster shared assets. "
    #                 "(https://github.com/michimussato/dagster-shared).",
    #     default="0.0.0.0",
    # )

    # Todo
    # dagster_enable_openstudiolandscapes_job_processor: bool = Field(
    #     description="Enable the OpenStudioLandscapes Dagster job processor. "
    #                 "(https://github.com/michimussato/dagster-job-processor).",
    #     default="0.0.0.0",
    # )

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

    # EXPANDABLE PATHS
    @property
    def dagster_postgres_db_install_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.dagster_postgres_db_install_dir}...")
        ret = pathlib.Path(
            self.dagster_postgres_db_install_dir.expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = get_config_str(
    Config=Config,
)

