from pprint import pprint
from typing import Optional, List

from src.quad_linked_list import QuadNode, QuadLinkedList


class ExactCoverSolver:

    def __init__(self, binary_matrix: List[List[bool]]):
        self.finished = False
        self.potential_solutions = []
        self.binary_matrix = binary_matrix
        self.sparse_list = QuadLinkedList.from_matrix(binary_matrix)

    def get_exact_cover_board(self) -> List[List[bool]]:
        """
        This function produces the exact cover board based on the solutions found at the end of the run
        """
        exact_cover_board = []
        for n in self.potential_solutions:
            exact_cover_board.append(self.binary_matrix[n.payload])
        return exact_cover_board

    def select_initial_nodes(self, row_node: QuadNode):
        """
        This function receives a node and selects it.
        It makes sure that the solution will contain the specified node in the solution.
        """
        cover(row_node.header_node)
        right_node = row_node.right_node
        while right_node is not row_node:
            cover(right_node.header_node)
            right_node = right_node.right_node
        self.potential_solutions.append(row_node)

    def algorithm_x(self) -> Optional[List[List[bool]]]:
        """
        This function applies algorithm x to the sparse list. It produces only one solution, even if many can be found.
        """
        exact_cover_board = None
        if self.sparse_list.head_node.left_node is self.sparse_list.head_node and self.sparse_list.head_node.right_node is self.sparse_list.head_node:
            print("---- SOLVED ----")
            self.finished = True
            return self.get_exact_cover_board()

        column: QuadNode = choose_column(self.sparse_list)
        cover(column)

        row_node: Optional[QuadNode] = column.bottom_node
        while row_node is not column and not self.finished:
            self.potential_solutions.append(row_node)

            right_node = row_node.right_node

            # Trying a specific node
            while right_node is not row_node:
                cover(right_node.header_node)
                right_node = right_node.right_node
            exact_cover_board = self.algorithm_x()

            # The node we tried didn't work
            right_node = row_node.right_node
            while right_node is not row_node:
                uncover(right_node.header_node)
                right_node = right_node.right_node

            self.potential_solutions.pop()
            row_node = row_node.bottom_node
        uncover(column)
        return exact_cover_board


def choose_column(cover_board: QuadLinkedList) -> QuadNode:
    return cover_board.head_node.right_node


def cover(column_node: QuadNode):
    column_node.right_node.left_node = column_node.left_node
    column_node.left_node.right_node = column_node.right_node

    row_node = column_node.bottom_node
    while row_node is not column_node:
        right_node = row_node.right_node
        while right_node is not row_node:
            right_node.top_node.bottom_node = right_node.bottom_node
            right_node.bottom_node.top_node = right_node.top_node

            right_node = right_node.right_node
        row_node = row_node.bottom_node


def uncover(column_node: QuadNode):
    row_node = column_node.top_node
    while row_node is not column_node:
        left_node = row_node.left_node
        while left_node is not row_node:
            left_node.top_node.bottom_node = left_node
            left_node.bottom_node.top_node = left_node

            left_node = left_node.left_node
        row_node = row_node.top_node

    column_node.right_node.left_node = column_node
    column_node.left_node.right_node = column_node


if __name__ == '__main__':
    # sample_board = [
    #     [1, 0, 0, 1, 0, 0, 1],
    #     [1, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 1, 1, 0, 1],
    #     [0, 0, 1, 0, 1, 1, 0],
    #     [0, 1, 1, 0, 0, 1, 1],
    #     [0, 1, 0, 0, 0, 0, 1],
    # ]
    sample_board = [
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 0, 1, 1],
    ]
    bool_mat = [list(map(bool, x)) for x in sample_board]
    exc = ExactCoverSolver(bool_mat)
    exc.select_initial_nodes(exc.sparse_list.head_node.right_node.bottom_node)
    print(exc.algorithm_x())
    # pprint([list(map(int, x)) for x in exc.algorithm_x()])
