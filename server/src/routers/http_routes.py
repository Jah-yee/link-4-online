from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse
from pathlib import Path
from room_manager import RoomManager, Room
from schemas.network import CanJoinRoomMessage, CreateRoomMessage
from typing import Union
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="", tags=["http"])

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
