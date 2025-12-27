from __future__ import annotations

from typing import Any

from core.config import Settings
from core.model import ModelRunner


class ImageProcessor:
    """OpenCV + model inference pipeline (Stage 1 skeleton)."""

    def __init__(self, settings: Settings, model: ModelRunner) -> None:
        self.settings = settings
        self.model = model

    def process_bytes(self, image_bytes: bytes) -> dict[str, Any]:
        raise NotImplementedError
