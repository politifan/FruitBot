from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    bot_token: str
    data_dir: Path
    model_path: Path
    log_level: str
    max_upload_mb: int
    history_default_limit: int
    image_size: int
    image_format: str
    device: str

    @property
    def images_dir(self) -> Path:
        return self.data_dir / "files" / "images"


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def get_settings() -> Settings:
    data_dir = Path(_env("DATA_DIR", "./data")).resolve()
    model_path = Path(_env("MODEL_PATH", "./model.pth")).resolve()
    return Settings(
        bot_token=_env("BOT_TOKEN", ""),
        data_dir=data_dir,
        model_path=model_path,
        log_level=_env("LOG_LEVEL", "INFO"),
        max_upload_mb=int(_env("MAX_UPLOAD_MB", "10")),
        history_default_limit=int(_env("HISTORY_DEFAULT_LIMIT", "10")),
        image_size=int(_env("IMAGE_SIZE", "224")),
        image_format=_env("IMAGE_FORMAT", "jpg"),
        device=_env("DEVICE", "cpu"),
    )


def ensure_directories(settings: Settings) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.images_dir.mkdir(parents=True, exist_ok=True)
