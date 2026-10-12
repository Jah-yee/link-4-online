from fastapi import (
    FastAPI,
    Request,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from pathlib import Path
import secrets
from typing import Callable, Awaitable
import os
import logging

logger = logging.getLogger("uvicorn.error")


from routers import http_routes, websocket_routes

# DISTDIR = Path(__file__).resolve().parent / ".." / ".." / "dist"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_csp_nonce(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    nonce = secrets.token_urlsafe(16)
    request.state.nonce = nonce

    response = await call_next(request)

    csp_value = (
        f"script-src 'nonce-{nonce}' 'strict-dynamic' https:; object-src 'none';"
    )
    response.headers["Content-Security-Policy"] = csp_value

    return response


# app.mount(
#     "/assets", StaticFiles(directory=DISTDIR / "assets", html=True), name="assets"
# )


app.include_router(http_routes.router)

app.include_router(websocket_routes.router)


if __name__ == "__main__":
    host =  os.getenv("APP_HOST", "127.0.0.1")
    app_env = os.getenv("APP_ENV", "development")
    is_dev_environment = app_env == "development"
    uvicorn.run("server:app", host=host , port=8000, reload=is_dev_environment)
