from __future__ import annotations

from typing import Any

from core.config import Settings


def create_app(settings: Settings) -> Any:
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise RuntimeError("FastAPI is required to run the web app.") from exc

    app = FastAPI(title="FruitBot")
    app.state.settings = settings

    @app.get("/")
    def root() -> dict[str, str]:
        return {"status": "ok"}

    return app
