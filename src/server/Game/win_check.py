import re
from schemas.game import (
    Board,
    BoardSell,
    WinPattern,
    WinningLine,
    PlayerNumber,
    Position,
    Direction,
    DirectionDownLeft,
    DirectionDownRight,
    DirectionDown,
    DirectionRight,
)
import logging

logger = logging.getLogger("uvicorn.error")

def get_col_direction_list(board: Board, x: int):
    col_direction_list: list[BoardSell] = []
    board_height = 6
    for i in range(board_height - 1, -1, -1):
        col_direction_list.append(board.root[i][x])
    return col_direction_list


def _has_linked_4(target_list: list[BoardSell], player_num: PlayerNumber):
    pattern = rf"{player_num.root}{{4,}}"
    target_text = "".join(map(str, [sell.root for sell in target_list]))
    rezult = re.search(pattern, target_text)
    if rezult:
        return rezult
    else:
        return None


def _wincheck_horizoontal(board: Board, player_num: PlayerNumber) -> WinPattern | None:
    board_height = 6
    # logger.info("wincheck_horizontal",player_num)
    for i in range(board_height):
        rezult = _has_linked_4(board.root[i], player_num)
        if rezult:
            search_start_position = (i, 0)
            # logger.info("rezult",rezult,"len",len(rezult.group(0)),rezult.span()[0])
            distance_startposition_and_search_start_position = rezult.span()[0]
            # logger.info("距離", distance_startposition_and_search_start_position)
            start_position = (
                search_start_position[0]
                + (
                    DirectionRight((0, 1)).root[0]
                    * distance_startposition_and_search_start_position
                ),
                search_start_position[1]
                + (
                    DirectionRight((0, 1)).root[1]
                    * distance_startposition_and_search_start_position
                ),
            )
            return WinPattern(
                startPosition=Position(start_position),
                direction=Direction(DirectionRight(root=(0, 1))),
                len=len(rezult.group(0)),
            )
    return None


def _wincheck_vertical(board: Board, player_num: PlayerNumber) -> WinPattern | None:
    # logger.info("wincheck_vertical", player_num)
    board_width = 7
    for i in range(board_width):
        rezult = _has_linked_4(get_col_direction_list(board, i), player_num)
        if rezult:
            search_start_position = (0, i)
            distance_start_position_and_search_start_position = 6 - rezult.span()[1]
            # logger.info("距離", distance_start_position_and_search_start_position,rezult)
            start_position = (
                search_start_position[0]
                + (
                    DirectionDown((1, 0)).root[0]
                    * distance_start_position_and_search_start_position
                ),
                search_start_position[1]
                + (
                    DirectionDown((1, 0)).root[1]
                    * distance_start_position_and_search_start_position
                ),
            )
            return WinPattern(
                startPosition=Position(start_position),
                direction=Direction(DirectionDown((1, 0))),
                len=len(rezult.group(0)),
            )
    return None


def _get_ascending_diagonal(start_position: tuple[int, int], board: Board):
    ascending_diagonal_list: list[BoardSell] = []
    y = start_position[0]
    x = start_position[1]
    while y <= 5 and x >= 0:
        ascending_diagonal_list.append(board.root[y][x])
        y += 1
        x -= 1
    return ascending_diagonal_list


def _get_descending_diagonal(start_position: tuple[int, int], board: Board):
    # pprint.plogger.info(board)
    descending_diagonal_list: list[BoardSell] = []
    y = start_position[0]
    x = start_position[1]
    # logger.info(f"({y},{x})")
    while y <= 5 and x <= 6:
        # logger.info(f"({y},{x})")
        descending_diagonal_list.append(board.root[y][x])
        y += 1
        x += 1
    return descending_diagonal_list


def _wincheck_ascending_diagonal(
    board: Board, player_num: PlayerNumber
) -> WinPattern | None:
    # logger.info("wincheck_ascending_diagonal")
    search_start_position_list: list[tuple[int, int]] = [
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 6),
        (2, 6),
    ]

    for search_start_position in search_start_position_list:
        target_list: list[BoardSell] = _get_ascending_diagonal(
            search_start_position, board
        )
        # logger.info(target_list,len(target_list))
        # logger.info("ascending", search_start_position, target_list)
        rezult = _has_linked_4(target_list, player_num)
        if rezult:
            distance_startposition_and_search_start_position = rezult.span()[0]
            # logger.info("距離", distance_startposition_and_search_start_position)
            start_position = (
                search_start_position[0]
                + (
                    DirectionDownLeft((1, -1)).root[0]
                    * distance_startposition_and_search_start_position
                ),
                search_start_position[1]
                + (
                    DirectionDownLeft((1, -1)).root[1]
                    * distance_startposition_and_search_start_position
                ),
            )
            return WinPattern(
                startPosition=Position(start_position),
                direction=Direction(DirectionDownLeft((1, -1))),
                len=len(rezult.group(0)),
            )
    return None


def _wincheck_descending_diagonal(
    board: Board, player_num: PlayerNumber
) -> WinPattern | None:
    # logger.info("wincheck_descending_diagonal")
    search_start_position_list: list[tuple[int, int]] = [
        (0, 3),
        (0, 2),
        (0, 1),
        (0, 0),
        (1, 0),
        (2, 0),
    ]
    for search_start_position in search_start_position_list:
        target_list: list[BoardSell] = _get_descending_diagonal(
            search_start_position, board
        )
        # logger.info(target_list,len(target_list))
        # logger.info("desending", search_start_position, target_list)
        rezult = _has_linked_4(target_list, player_num)
        if rezult:
            distance_startposition_and_search_start_position = rezult.span()[0]
            # logger.info("距離", distance_startposition_and_search_start_position)
            start_position = (
                search_start_position[0]
                + (
                    DirectionDownRight((1, 1)).root[0]
                    * distance_startposition_and_search_start_position
                ),
                search_start_position[1]
                + (
                    DirectionDownRight((1, 1)).root[1]
                    * distance_startposition_and_search_start_position
                ),
            )
            return WinPattern(
                startPosition=Position(start_position),
                direction=Direction(DirectionDownRight((1, 1))),
                len=len(rezult.group(0)),
            )
    return None


def wincheck(board: Board) -> WinningLine:
    logger.info("wincheck")
    linked_4_list: WinningLine = WinningLine([])
    for i in range(1, 2 + 1):
        if i in (1, 2):
            player_num = PlayerNumber(i)
            if linked_4_list.root is None:
                return WinningLine([])

            def addWinPattern(item: WinPattern | None):
                if item is not None and linked_4_list.root is not None:
                    linked_4_list.root.append(item)

            addWinPattern(_wincheck_horizoontal(board, player_num))
            addWinPattern(_wincheck_vertical(board, player_num))
            addWinPattern(_wincheck_ascending_diagonal(board, player_num))
            addWinPattern(_wincheck_descending_diagonal(board, player_num))

    logger.info(f"linked_4_list:filter:befor {linked_4_list}")
    logger.info(f"linked_4_list:filter:after {linked_4_list}")
    return linked_4_list
