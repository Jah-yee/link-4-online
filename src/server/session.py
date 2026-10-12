from fastapi import WebSocket
from pydantic import ValidationError
from schemas.game import PlayerNumber
from schemas.network import (
    WebsocketMessage,
    UserMessage,
    GameActionPutMessage,
    UserInfoMessage,
)
from debounce import Debounce
import logging

logger = logging.getLogger("uvicorn.error")


class Session:
    def __init__(self, id: int, websocket: WebSocket, target_room_id: int):
        self.id = id
        self.ws = websocket
        self.ready_start_game: bool = False
        self.target_room_id = target_room_id
        self._debounce_time_secound = 3 * 60
        self._debounce = Debounce(self._debounce_time_secound, self._debounce_calllback)
        if not self.get_target_room():
            raise ValueError(
                f"RoomManager is not have room. room_id:{self.target_room_id}"
            )

    def get_target_room(self):
        from room_manager import RoomManager

        return RoomManager.search_room_by_id(self.target_room_id)

    async def close(self):
        try:
            await self.ws.close()
        except RuntimeError:
            logger.info("session ws did closed")

    async def handlle_message(self, user_message: UserMessage):
        from session_manager import SessionManager

        logger.info(f"message: {user_message} room_id: {self.target_room_id}")
        match user_message.root.action:
            case "JOIN":
                await self.join_room()
            case "CANJOIN":
                await self.can_join_room()
            case "CANGAMESTART":
                await self.can_game_start()
            case "GAMESTART":
                await self.game_start()
            case "EXITROOM":
                await SessionManager.close_session(self.id)
            case "GAMEACTION":
                try:
                    GameActionPut_message = GameActionPutMessage.model_validate(
                        user_message.root
                    )
                    await self.game_action(GameActionPut_message)
                    logger.info("END GAMEACTION")
                except ValidationError as e:
                    logger.info(f"not GameActionPut errpr {e}")
            case "USERINFO":
                try:
                    UserInfo_message = UserInfoMessage.model_validate(user_message.root)
                    await self.set_ready_start_game(UserInfo_message.readyStartGame)
                except:
                    pass
            case "GAMEFINISH":
                logger.info("sesssion gmae finish")
                await self.finishGame()
            case _:
                pass
        self._debounce.resetTimer()

    async def join_room(self):
        try:
            from room_manager import RoomManager

            joind_room = await RoomManager.join_room(self.target_room_id, self)

            target_room = self.get_target_room()
            if target_room:
                logger.info(f"room session_list len {len(target_room.session_list)}")

            await joind_room.broadcast(WebsocketMessage("ROOMINFO"))
            await joind_room.broadcast(WebsocketMessage("GAMEINFO"))
        except ValueError:
            pass

    async def can_join_room(self):
        from room_manager import RoomManager

        return RoomManager.can_join_room(self.target_room_id)

    async def can_game_start(self):
        target_room = self.get_target_room()
        if target_room:
            return target_room.can_game_start()

    async def game_start(self):
        target_room = self.get_target_room()
        if target_room and target_room.can_game_start():
            target_room.game_start()
            try:
                await target_room.broadcast(WebsocketMessage("GAMESTART"))
                await target_room.broadcast(WebsocketMessage("GAMEINFO"))
                await target_room.broadcast(WebsocketMessage("ROOMINFO"))
            except RuntimeError as e:
                logger.info(f"runtime error: {e}")

    async def exit_room(self):
        target_room = self.get_target_room()
        if target_room:
            if target_room.exists_session(self):
                await target_room.exit(self)
            await self.close()
        else:
            raise ValueError(f"room is not found. room_id:{self.target_room_id}")

    def get_player_number(self) -> PlayerNumber | None:
        target_room = self.get_target_room()
        if target_room:
            return target_room.get_player_number(self)
        else:
            return None

    async def game_action(self, message: GameActionPutMessage):
        logger.info(f"game_action {self.get_player_number()}")

        target_room = self.get_target_room()

        player_number = self.get_player_number()
        if target_room and isinstance(player_number, PlayerNumber):
            target_room.game.put(message.x, player_number)
            await target_room.broadcast(WebsocketMessage("GAMEINFO"))

    async def set_ready_start_game(self, new_state: bool):
        self.ready_start_game = new_state
        target_room = self.get_target_room()
        if target_room:
            await target_room.broadcast(WebsocketMessage("ROOMINFO"))

    async def finishGame(self):
        target_room = self.get_target_room()
        if target_room:
            await target_room.finish_game()

    async def _debounce_calllback(self):
        await self.exit_room()
