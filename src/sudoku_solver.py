from pprint import pprint
from typing import List, Optional

from src.algorithm_x import ExactCoverSolver
from src.exact_cover import create_constraint_board
from src.quad_linked_list import QuadNode


def solve(unsolved_board: List[List[int]]) -> Optional[List[List[int]]]:
    constraint_board: List[List[bool]] = create_constraint_board(len(unsolved_board[0]))
    solver = ExactCoverSolver(constraint_board)
    cover_initial_state(unsolved_board, solver)

    solution = solver.algorithm_x()

    if solution:
        return convert_to_sudoku(solution, len(unsolved_board[0]))
    else:
        return None


def convert_to_sudoku(solution_matrix: List[QuadNode], dimensions) -> List[List[int]]:
    """
    This function converts the list of exact cover row nodes to an actual sudoku board.
    """
    solution_board: Optional[List[List[Optional[int]]]] = [[None for _ in range(dimensions)] for _ in range(dimensions)]

    for node in solution_matrix:
        solution_board[(node.payload // (dimensions**2))][(node.payload // dimensions) % dimensions] = (node.payload % dimensions) + 1
    return solution_board


def cover_initial_state(unsolved_board: List[List[int]], solver: ExactCoverSolver):
    """
    This function covers the initial states of the Sudoku board.
    """
    def get_row_node(number, board_row, board_column) -> QuadNode:
        """
        Given the number, the row in the board, and the column in the board, this function navigates to the correct
        row in the exact cover QuadLinkedList and returns the node so that it can be initially selected.
        """
        start_node = solver.sparse_list.head_node.right_node

        for _ in range(board_row * len(unsolved_board[0])):
            start_node = start_node.right_node

        for _ in range(board_column):
            start_node = start_node.right_node

        for _ in range(number):
            start_node = start_node.bottom_node
        return start_node

    initial_nodes = []
    for row_index, row in enumerate(unsolved_board):
        for column, num in enumerate(row):
            if 1 <= num <= 9:
                initial_nodes.append(get_row_node(num, row_index, column))

    for node in initial_nodes:
        solver.select_initial_node(node)


if __name__ == '__main__':
    board = [
        [0, 2, 3, 0],
        [0, 0, 0, 0],
        [3, 4, 0, 2],
        [2, 0, 0, 0],
    ]
    pprint(solve(board))
