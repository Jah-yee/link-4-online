from fastapi import WebSocket
from session import Session
import secrets
import logging

logger = logging.getLogger("uvicorn")

class SessionManager:
    session_list: list[Session] = []

    def __new__(cls):
        raise TypeError(f"{cls.__name__} is can not create instance")

    @classmethod
    def create_session(cls, ws: WebSocket, target_room_id: int):
        new_id = secrets.randbelow(10000)

        def exists():
            return any(session.id == new_id for session in SessionManager.session_list)

        while exists():
            new_id = secrets.randbelow(10000)
        cls.session_list.append(Session(new_id, ws, target_room_id))
        logger.info(f"RM create_room() room_id:{target_room_id} session_id:{new_id}")
        return cls.search_session_by_id(new_id)

    @classmethod
    def search_session_by_id(cls, id: int) -> None | Session:
        for session in cls.session_list:
            if session.id == id:
                return session
        return None

    @classmethod
    async def close_session(cls, id: int):
        target_session = cls.search_session_by_id(id)
        if target_session:
            await target_session.exit_room()
            return cls.session_list.remove(target_session)
        raise ValueError(f"{cls.__name__} have not session. id:{id}")
