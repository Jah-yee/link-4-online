from typing import Literal, Annotated
from pydantic import BaseModel, RootModel, Field
from schemas.game import GameState, GameData


class JoinRoomMessage(BaseModel):
    action: Literal["JOIN"] = "JOIN"


class CanJoinRoomMessage(BaseModel):
    action: Literal["CANJOIN"] = "CANJOIN"
    roomId: int


class CreateRoomMessage(BaseModel):
    action: Literal["CREATE"] = "CREATE"


class ExitRoomMessage(BaseModel):
    action: Literal["EXITROOM"] = "EXITROOM"


class CanGameStartMessage(BaseModel):
    action: Literal["CANGAMESTART"] = "CANGAMESTART"


class GameStartMessage(BaseModel):
    action: Literal["GAMESTART"] = "GAMESTART"


class GameActionPutMessage(BaseModel):
    action: Literal["GAMEACTION"] = "GAMEACTION"
    gameAction: Literal["PUT"] = "PUT"
    x: Literal[0, 1, 2, 3, 4, 5, 6, 7]


class UserInfoMessage(BaseModel):
    action: Literal["USERINFO"] = "USERINFO"
    readyStartGame: bool


class FinishGameMessage(BaseModel):
    action: Literal["GAMEFINISH"] = "GAMEFINISH"


UserMessageUnion = (
    JoinRoomMessage
    | CanJoinRoomMessage
    | ExitRoomMessage
    | CanGameStartMessage
    | GameStartMessage
    | GameActionPutMessage
    | UserInfoMessage
    | FinishGameMessage
)


class UserMessage(
    RootModel[Annotated[UserMessageUnion, Field(discriminator="action")]]
):
    pass


class WebsocketMessage(
    RootModel[Literal["ROOMINFO", "GAMEINFO", "GAMESTART", "GAMEFINISH"]]
):
    pass


class WebsocketMessageRoomInfo(BaseModel):
    message: Literal["ROOMINFO"]
    numberOfSession: int
    gameState: GameState
    roomId: int
    canGameStart: bool
    remotePlayerReady: bool


class WebsocketMessageGameStart(BaseModel):
    message: Literal["GAMESTART"]


class WebsocketMessageGameFinish(BaseModel):
    message: Literal["GAMEFINISH"]


class WebsocketMessageGameInfo(BaseModel):
    message: Literal["GAMEINFO"]
    gameData: GameData


WebsocketMessageUnion = (
    WebsocketMessageRoomInfo
    | WebsocketMessageGameFinish
    | WebsocketMessageGameStart
    | WebsocketMessageGameInfo
)
