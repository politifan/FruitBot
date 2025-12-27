# FruitBot Stage 0 Specification

This document captures the initial decisions for the project scope, data model,
module boundaries, and runtime approach. It is the baseline for Stage 1 work.

## 1) Scope
Goals:
- Telegram bot for photo classification: apple vs orange.
- Web UI + REST API for upload, history, and stats.
- Single shared JSON storage (no database).
- Simple ML model: transfer learning with ResNet18.

Non-goals:
- Video processing.
- Object detection.
- Multi-class classification.
- External DBs or cloud storage.

## 2) Data Storage
Directory layout:
```
data/
  analyses.json
  users.json
  files/
    images/
```

analyses.json (array of objects):
```json
{
  "id": "uuid-1234",
  "timestamp": "2025-12-27T15:43:22Z",
  "user_id": 123456789,
  "source": "telegram",
  "image_path": "files/images/uuid-1234.jpg",
  "predicted_class": "apple",
  "confidence": 0.96,
  "processing_time_sec": 1.2
}
```

users.json (object keyed by user_id as string):
```json
{
  "123456789": {
    "total": 42,
    "apple": 25,
    "orange": 17,
    "last_seen": "2025-12-27T15:43:22Z"
  }
}
```

Storage rules:
- All file paths are relative to `data/`.
- JSON writes are protected with filelock and atomic replace.
- Missing files or malformed JSON -> initialize empty structures.
- Store only one compressed image per analysis, using the training input format
  (size + encoding). Annotated images are generated in memory and not persisted.

## 3) Runtime Architecture
Single process, one asyncio event loop:
- FastAPI app served by Uvicorn programmatically.
- Aiogram bot runs polling in the same loop.
- Shared `storage` and `processor` modules.

Proposed approach:
- `main.py` creates tasks: `uvicorn_server.serve()` + `dp.start_polling(...)`
- Graceful shutdown on SIGINT/SIGTERM.

## 4) Module Responsibilities
core/config.py
- Load env vars with defaults.
- Centralize paths and settings.

core/storage.py
- CRUD for analyses.json and users.json.
- Save a single compressed image per analysis.
- Provide pagination helpers.

core/model.py
- Load Torch model, run inference.
- Define class mapping: ["apple", "orange"].

core/processor.py
- OpenCV preprocessing + model inference.
- Annotate image with class + confidence (in-memory, not stored).
- Return metadata for storage.

web/routes.py
- API endpoints and page routes.
- Jinja2 rendering and static files.

bot/handlers.py
- Commands: /start, /help, /stats, /history
- Photo handler -> processor + storage

## 5) API Surface
REST API:
- GET /api/history?limit=20&offset=0
- GET /api/analysis/{id}
- POST /api/upload (multipart image)

Web pages:
- /
- /analysis/{id}
- /stats
- /upload

## 6) Config (initial)
Environment variables:
- BOT_TOKEN
- DATA_DIR (default: ./data)
- MODEL_PATH (default: ./model.pth)
- LOG_LEVEL (default: INFO)
- MAX_UPLOAD_MB (default: 10)
- HISTORY_DEFAULT_LIMIT (default: 10)
- IMAGE_SIZE (default: 224)
- IMAGE_FORMAT (default: jpg)
- DEVICE (default: cpu, use cuda if available)

## 7) Logging
Simple structured logs to stdout:
- timestamp, level, module, message
- errors include exception traceback

## 8) Dependencies (initial targets)
Runtime:
- python 3.11+
- torch, torchvision
- aiogram 3.x
- fastapi
- opencv-python
- jinja2
- python-multipart
- filelock
- uvicorn

Dev/test (optional):
- pytest
- ruff (or black/flake8)

## 9) Decisions (Stage 0)
1) `/history` default is 10.
2) Histories are local: web shows only source=web; bot history is per user_id.
3) Default device is CPU; use GPU if available.
4) Max upload size is 10 MB.
5) Store only one compressed image in the training input format; no originals or
   annotated images are persisted.
