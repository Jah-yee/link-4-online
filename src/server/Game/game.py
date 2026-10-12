from Game.win_check import wincheck
from schemas.game import GameData, GameState, PlayerNumber, Board, BoardSell
import logging

logger = logging.getLogger("ubvicorn.error")


class Link_4:
    def __init__(self):
        self.gameState: GameState = GameState("unstarted")
        self.now_turn: PlayerNumber = PlayerNumber(1)
        self._board: Board = Board([[BoardSell(0) for _ in range(7)] for _ in range(6)])

    @property
    def board_height(self):
        return 6

    @property
    def board_width(self):
        return 7

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board: Board):
        logger.info("game.boardが変更されました")
        self._board = new_board

    def game_start(self):
        self.gameState.root = "playing"
        self.now_turn.root = 1
        self._board = Board([[BoardSell(0) for _ in range(7)] for _ in range(6)])

    def put(self, x: int, player: PlayerNumber):
        logger.info(f"put {x} player: {player}")
        if (
            self._get_put_height(x) == self.board_height
            or self.gameState.root != "playing"
        ):
            return
        if self.now_turn.root != player.root:
            return
        # 置く高さ
        put_y_index = self.board_height - self._get_put_height(x) - 1
        logger.info(f"put_y: {put_y_index}")
        if put_y_index < 0:
            return
        self._board.root[put_y_index][x].root = self.now_turn.root
        winningLine = wincheck(self._board)
        if winningLine.root != None and len(winningLine.root) >= 1:
            return self._gameSet()
        if all(
            [
                self._get_put_height(x) == self.board_height
                for x in range(self.board_width)
            ]
        ):
            return self._gameSet()
        else:
            return self._turn_change()

    def _turn_change(self):
        if self.now_turn.root == 1:
            self.now_turn.root = 2
        else:
            self.now_turn.root = 1
        logger.info(f"not turn:{self.now_turn}")

    def get_col_direction_list(self, x: int):
        col_direction_list: list[int] = []
        for i in range(self.board_height - 1, -1, -1):
            col_direction_list.append(self._board.root[i][x].root)
        return col_direction_list

    def _get_put_height(self, x: int):
        col_direction_list = self.get_col_direction_list(x)
        return self.board_height - col_direction_list.count(0)

    def _gameSet(self):
        if self.gameState.root == "playing":
            self.gameState.root = "gameset"

    def reset(self):
        self.gameState.root = "unstarted"
        self.now_turn.root = 1
        self._board = Board([[BoardSell(0) for _ in range(7)] for _ in range(6)])

    @property
    def get_board_support_JSON(self):
        return [[sell.root for sell in row] for row in self.board.root]

    def get_game_data(self, player: PlayerNumber) -> GameData:
        logger.info(f"get_game_data: {self.gameState.root}")
        return GameData(
            board=self._board,
            playerNum=player,
            yourTurn=self.now_turn.root == player.root
            and self.gameState.root == "playing",
            gameState=self.gameState,
            winningLine=wincheck(self.board),
        )
