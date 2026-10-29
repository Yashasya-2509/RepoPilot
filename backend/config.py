from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RepoPilot"
    app_env: str = "development"
    log_level: str = "INFO"
    workspace_root: Path = Path("./workspaces")
    database_path: Path = Path("./artifacts/repopilot.sqlite3")
    max_file_bytes: int = 1_000_000
    max_files: int = 5_000
    max_search_results: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.workspace_root = settings.workspace_root.expanduser().resolve()
    settings.database_path = settings.database_path.expanduser().resolve()
    return settings
