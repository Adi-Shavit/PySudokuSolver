from typing import Optional, List

from src.quad_linked_list import QuadNode, QuadLinkedList


class ExactCoverSolver:

    def __init__(self, binary_matrix: List[List[bool]]):
        self.finished = False
        self.potential_solutions = []
        self.binary_matrix = binary_matrix
        self.sparse_list = QuadLinkedList.from_matrix(binary_matrix)

    def get_exact_cover_solution(self) -> List[QuadNode]:
        """
        This function returns a list of nodes where each node is a row in the exact cover board solution.
        """
        actual_solution = []
        for n in self.potential_solutions:
            actual_solution.append(n)
        return actual_solution

    def select_initial_node(self, row_node: QuadNode):
        """
        This function receives a node and selects it.
        It makes sure that the solution will contain the specified node in the solution.
        It makes sure that the row the node belongs to will be in the exact cover board.
        """
        cover(row_node.header_node)
        right_node = row_node.right_node
        while right_node is not row_node:
            cover(right_node.header_node)
            right_node = right_node.right_node
        self.potential_solutions.append(row_node)

    def algorithm_x(self) -> Optional[List[QuadNode]]:
        """
        This function applies algorithm x to the sparse list. It produces only one solution, even if many can be found.
        """
        exact_cover_board = None
        if self.sparse_list.head_node.left_node is self.sparse_list.head_node and self.sparse_list.head_node.right_node is self.sparse_list.head_node:
            self.finished = True
            return self.get_exact_cover_solution()

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
    """
    This function performs the cover logic using the dancing links trick.
    """
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
    """
    This function performs the uncovers a previously covered column.
    """
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
