from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.config import Settings


@dataclass
class AnalysisRecord:
    id: str
    timestamp: str
    user_id: int | None
    source: str
    image_path: str
    predicted_class: str
    confidence: float
    processing_time_sec: float


class Storage:
    """JSON storage interface (Stage 1 skeleton)."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.analyses_path = settings.data_dir / "analyses.json"
        self.users_path = settings.data_dir / "users.json"

    def save_analysis(self, record: AnalysisRecord) -> None:
        raise NotImplementedError

    def list_analyses(self, limit: int, offset: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_analysis(self, analysis_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    def update_user_stats(self, user_id: int, predicted_class: str) -> None:
        raise NotImplementedError

    def get_user_history(self, user_id: int, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError
