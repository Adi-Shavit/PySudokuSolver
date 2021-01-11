from typing import List

import numpy as np


def create_constraint_board(dimensions: int) -> List[List[bool]]:
    """
    This function will create the exact cover board given a board input size.
    It'll do so by calculating the 4 parts of the exact cover board for Sudoku:
        1. Row-Column values
        2. Row-Number values
        3. Column-Number values
        4. Box-Number values
    :param int dimensions: The dimensions of the Sudoku Board
    :return:
    """
    cover_board: np.ndarray = np.array([[0] * 4 * (dimensions ** 2)] * (dimensions ** 3))
    __row_column(dimensions, cover_board)
    __row_number(dimensions, cover_board)
    __column_number(dimensions, cover_board)
    __box_number(dimensions, cover_board)
    return cover_board.astype(bool).tolist()


def __row_column(dimensions: int, cover_board: np.ndarray):
    for col in range(dimensions ** 2):
        for row in range(dimensions):
            cover_board[row + col * dimensions][col] = 1


def __row_number(dimensions: int, cover_board: np.ndarray):
    # col_offset represents the next chunk being calculated in the matrix
    col_offset = dimensions ** 2
    for col in range(dimensions ** 2, 2 * dimensions ** 2):
        adjusted_col = col % dimensions ** 2
        column_block = adjusted_col // dimensions
        for row in range(dimensions):
            x = row + (column_block * dimensions) + col_offset
            y = adjusted_col * dimensions + row
            cover_board[y][x] = 1


def __column_number(dimensions: int, cover_board: np.ndarray):
    col_offset = 2 * dimensions ** 2

    for col in range(2 * dimensions ** 2, 3 * (dimensions ** 2)):
        adjusted_col = col % dimensions ** 2
        for row in range(dimensions):
            x = (row + adjusted_col * dimensions) % dimensions ** 2 + col_offset
            y = row + adjusted_col * dimensions
            cover_board[y][x] = 1


def __box_number(dimensions: int, cover_board: np.ndarray):
    s_size = int(np.sqrt(dimensions))
    col_offset = 3 * dimensions ** 2

    for col in range(3 * dimensions ** 2, 4 * dimensions ** 2):
        adjusted_col = col % dimensions ** 2
        column_block = ((adjusted_col // s_size) % s_size)
        for row in range(dimensions):
            x = col_offset + row + (column_block + (adjusted_col // (dimensions * s_size)) * s_size) * dimensions
            y = adjusted_col * dimensions + row
            cover_board[y][x] = 1
