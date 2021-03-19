from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath


class AppSettings(BaseSettings):
    base_dir: DirectoryPath = Path(__file__).parent.parent
    data_dir: Path = base_dir.joinpath("data")
    artifact_dir: Path = base_dir.joinpath("artifacts")
    metrics_dir: Path = base_dir.joinpath("metrics")

    def update_base(self, new_base_pth: DirectoryPath) -> None:
        """
        Update base_dir and the fields that depend on it (data_dir, artifact_dir, metrics_dir)

        Args:
            new_base_pth: The new base directory path.

        Returns: None

        """

        self.base_dir = new_base_pth
        self.data_dir = self.base_dir.joinpath("data")
        self.artifact_dir = self.base_dir.joinpath("artifacts")
        self.metrics_dir = self.base_dir.joinpath("metrics")

    class Config:
        validate_assignment = True


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()
