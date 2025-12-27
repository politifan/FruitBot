from __future__ import annotations

from pathlib import Path
from typing import Any


class ModelRunner:
    """PyTorch model wrapper (Stage 1 skeleton)."""

    def __init__(self, model_path: Path, device: str, image_size: int) -> None:
        self.model_path = model_path
        self.device = device
        self.image_size = image_size
        self.model: Any | None = None

    def load(self) -> None:
        raise NotImplementedError

    def predict(self, image_array: Any) -> tuple[str, float]:
        raise NotImplementedError
