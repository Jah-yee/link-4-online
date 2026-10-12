from Game.game import Link_4
from session import Session
from schemas.game import PlayerNumber
from schemas.network import (
    WebsocketMessage,
    WebsocketMessageGameStart,
    WebsocketMessageGameFinish,
    WebsocketMessageRoomInfo,
    WebsocketMessageGameInfo,
    WebsocketMessageUnion,
)
from debounce import Debounce
import logging

logger = logging.getLogger("uvicorn.error")


class Room:

    def __init__(self, id: int):
        from room_manager import RoomManager

        self.id = id
        self.session_list: list[Session] = []
        self.player_1: Session | None = None
        self.player_2: Session | None = None
        self._max_session: int = 2
        self._game = Link_4()
        self._debounce_time_secound: int = 5 * 60
        self._debounce = Debounce(
            self._debounce_time_secound, lambda: RoomManager.close_room(self.id)
        )

    @property
    def max_session(self):
        return self._max_session

    def game_start(self):
        self._game.game_start()
        self._debounce.resetTimer()

    def can_join(self) -> bool:
        return len(self.session_list) < self.max_session and (
            self.player_1 == None or self.player_2 == None
        )

    async def join(self, session: Session):
        from room_manager import RoomManager

        if self.can_join():
            self.session_list.append(session)
            if self.player_1 == None:
                self.player_1 = session
            elif self.player_2 == None:
                self.player_2 = session
            await self.broadcast(WebsocketMessage("ROOMINFO"))
            await self.broadcast(WebsocketMessage("GAMEINFO"))
            RoomManager.printRoomStatus()
            self._debounce.resetTimer()
            return self
        raise SystemError("can not join room")

    async def exit(self, session: Session):
        from room_manager import RoomManager

        logger.info(f"Room exit check exists: {self.exists_session(session)} {session in self.session_list}")
        if self.exists_session(session):
            if self.player_1 is session:
                self.player_1 = None
            if self.player_2 is session:
                self.player_2 = None
            self.session_list.remove(session)
            RoomManager.printRoomStatus()
            await self.broadcast(WebsocketMessage("ROOMINFO"))
            self._debounce.resetTimer()
            return True
        raise ValueError(
            f"session is not in session_list. room_id:{self.id},session_id:{session.id}"
        )

    def get_ws_message(
        self, message: WebsocketMessage, session: Session
    ) -> WebsocketMessageUnion | None:
        match message.root:
            case "ROOMINFO":
                remotePlayerReadyBool = False
                player_number = self.get_player_number(session)
                if isinstance(player_number, PlayerNumber) and player_number.root == 1:
                    if self.player_2:
                        remotePlayerReadyBool = self.player_2.ready_start_game
                else:
                    if self.player_1:
                        remotePlayerReadyBool = self.player_1.ready_start_game
                logger.info("get_ws_message ROOMINFO")
                return WebsocketMessageRoomInfo(
                    message="ROOMINFO",
                    numberOfSession=len(self.session_list),
                    gameState=self._game.gameState,
                    roomId=self.id,
                    canGameStart=self.can_game_start(),
                    remotePlayerReady=remotePlayerReadyBool,
                )
            case "GAMEINFO":
                player_number = session.get_player_number()
                logger.info(f"BROADCAST GAMEINFO player_number: {player_number}")
                logger.info(f"winningLine {player_number}")
                if isinstance(player_number, PlayerNumber):
                    return WebsocketMessageGameInfo(
                        message="GAMEINFO",
                        gameData=self._game.get_game_data(player_number),
                    )
                else:
                    return None
            case "GAMESTART":
                return WebsocketMessageGameStart(message="GAMESTART")
            case "GAMEFINISH":
                return WebsocketMessageGameFinish(message="GAMEFINISH")
            case _:
                pass

    def can_game_start(self) -> bool:
        all_player_ready = all(
            session.ready_start_game for session in self.session_list
        )
        if all(
            [
                len(self.session_list) == 2,
                isinstance(self.player_1, Session),
                isinstance(self.player_2, Session),
                self._game.gameState.root == "unstarted",
                all_player_ready,
            ]
        ):
            return True
        else:
            return False

    async def broadcast(self, message: WebsocketMessage):
        logger.info(f"BROADCAST message: {message}")
        for session in self.session_list:
            send_message = self.get_ws_message(message, session)
            if send_message != None:
                await session.ws.send_json(send_message.model_dump())
        logger.info(f"BROADCAST END message: {message}")

    @property
    def game(self):
        return self._game

    async def finish_game(self):
        if self.game.gameState.root == "gameset":
            for session in self.session_list:
                session.ready_start_game = False
            self.game.reset()
            await self.broadcast(WebsocketMessage("GAMEINFO"))
            await self.broadcast(WebsocketMessage("ROOMINFO"))
            await self.broadcast(WebsocketMessage("GAMEFINISH"))
            self._debounce.resetTimer()

    def get_player_number(self, session: Session) -> PlayerNumber | None:
        if session not in self.session_list:
            return None
        if self.player_1 is session:
            return PlayerNumber(1)
        if self.player_2 is session:
            return PlayerNumber(2)
        return None

    def exists_session(self, session: Session) -> bool:
        exists = any(item is session for item in self.session_list)
        return exists
