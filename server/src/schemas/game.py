from pydantic import RootModel, BaseModel
from typing import Literal


class GameState(RootModel[Literal["unstarted", "playing", "gameset"]]):
    pass


class BoardSell(RootModel[Literal[0, 1, 2]]):
    pass


class Board(RootModel[list[list[BoardSell]]]):
    pass


class PlayerNumber(RootModel[Literal[1, 2]]):
    pass


class Position(RootModel[tuple[int, int]]):
    pass


class DirectionDownLeft(RootModel[tuple[Literal[1], Literal[-1]]]):
    pass


class DirectionDownRight(RootModel[tuple[Literal[1], Literal[1]]]):
    pass


class DirectionDown(RootModel[tuple[Literal[1], Literal[0]]]):
    pass


class DirectionRight(RootModel[tuple[Literal[0], Literal[1]]]):
    pass


DirectionUnion = DirectionDownLeft | DirectionDownRight | DirectionDown | DirectionRight


class Direction(RootModel[DirectionUnion]):
    pass


class WinPattern(BaseModel):
    startPosition: Position
    direction: Direction
    len: int


class WinningLine(RootModel[list[WinPattern] | None]):
    pass


class GameData(BaseModel):
    board: Board
    playerNum: PlayerNumber
    yourTurn: bool
    gameState: GameState
    winningLine: WinningLine
