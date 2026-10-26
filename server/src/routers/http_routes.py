from os import eventfd_write

from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse
from pathlib import Path
from room_manager import RoomManager, Room
from schemas.network import CanJoinRoomMessage, CreateRoomMessage
from typing import Union
import logging

logger = logging.getLogger("uvicorn.error")

DISTDIR = Path(__file__).resolve().parent / ".." / ".." / ".." / "dist"

router = APIRouter(prefix="", tags=["http"])


@router.get("/")
def _(request: Request):
    nonce = request.state.nonce
    html_content = (DISTDIR / "index.html").read_text(encoding="utf-8")
    html_content = html_content.replace("__NONCE__", nonce)
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/room/{room_id:path}")
async def _(request: Request):
    logger.info(f"get room {request}")
    nonce = request.state.nonce
    html_content = (DISTDIR / "index.html").read_text(encoding="utf-8")
    html_content = html_content.replace("__NONCE__", nonce)
    return HTMLResponse(content=html_content, status_code=200)


@router.post("/room")
async def _(
    body: Union[CreateRoomMessage, CanJoinRoomMessage] = Body(
        ..., discriminator="action"
    )
):
    if isinstance(body, CreateRoomMessage):
        # body is CreateRoomBody
        new_room = RoomManager.create_room()
        if isinstance(new_room, Room):
            logger.info(f"CREATE ROOM id: {new_room.id}")
            return new_room.id
        return None
    else:
        # body is CanJoinRoomBody
        return RoomManager.can_join_room(body.roomId)
