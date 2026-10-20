from fastapi import (
    FastAPI,
    Request,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from pathlib import Path
from typing import Callable, Awaitable
import os
import logging

logger = logging.getLogger("uvicorn.error")


from routers import http_routes, websocket_routes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(http_routes.router)

app.include_router(websocket_routes.router)


if __name__ == "__main__":
    host =  os.getenv("APP_HOST", "127.0.0.1")
    app_env = os.getenv("APP_ENV", "development")
    is_dev_environment = app_env == "development"
    uvicorn.run("server:app", host=host , port=8000, reload=is_dev_environment)
