from session import Session
from room import Room

from typing import Literal
import secrets
import logging

logger = logging.getLogger("uvicorn.error")

class RoomManager:
    room_list: list[Room] = []
    room_list_max_len: Literal[100] = 100

    def __new__(cls):
        raise TypeError(f"{RoomManager.__name__} is can not create instance")

    @classmethod
    def create_room(cls):
        new_room_id = secrets.randbelow(10000)

        def exists() -> bool:
            return any(item.id == new_room_id for item in RoomManager.room_list)

        while exists():
            new_room_id = secrets.randbelow(10000)

        cls.room_list.append(Room(new_room_id))
        logger.info(f"RM create_room() room_id:{new_room_id}")
        RoomManager.printRoomStatus()
        return RoomManager.search_room_by_id(new_room_id)

    @classmethod
    def search_room_by_id(cls, room_id: int):
        for room in cls.room_list:
            if room.id == room_id:
                return room
        return None

    @classmethod
    def close_room(cls, room_id: int):
        target_room = cls.search_room_by_id(room_id)
        if isinstance(target_room, Room):
            cls.room_list.remove(target_room)
            RoomManager.printRoomStatus()
            if not isinstance(cls.search_room_by_id(room_id), Room):
                return True
            else:
                return False
        raise ValueError(f"{cls.__name__} have not room. room_id:{room_id}")

    @classmethod
    def can_join_room(cls, room_id: int):
        room = cls.search_room_by_id(room_id)
        if isinstance(room, Room) and room.can_join():
            return True
        else:
            return False

    @classmethod
    async def join_room(cls, room_id: int, session: Session):
        if cls.can_join_room(room_id):
            room = cls.search_room_by_id(room_id)
            if isinstance(room, Room):
                return await room.join(session)
            else:
                raise ValueError(f"{cls.__name__} have not room. room_id:{room_id}")
        raise ValueError(f"room can not join. room_id:{room_id}")

    @classmethod
    def printRoomStatus(cls):
        logger.info("---RoomStatus---")
        logger.info(f"room count:{len(RoomManager.room_list)}")
        logger.info(
            f"session count:{len(list((session for session in room.session_list) for room in RoomManager.room_list))}"
        )
        logger.info(" room id | session id")
        for room in RoomManager.room_list:
            logger.info(f" {room.id} | {[session.id for session in room.session_list]}")
        if len(RoomManager.room_list) == 0:
            logger.info("    NO ROOM      ")
        logger.info("-" * 17)
