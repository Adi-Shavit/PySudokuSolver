from __future__ import annotations
from typing import Optional, List


class QuadNode:
    def __init__(self, payload, right_node=None,
                 left_node=None, top_node=None, bottom_node=None):
        self.payload = payload

        # The reference to the next Nodes
        self.right_node: QuadNode = right_node
        self.left_node: QuadNode = left_node
        self.top_node: QuadNode = top_node
        self.bottom_node: QuadNode = bottom_node


class QuadLinkedList:
    def __init__(self):
        self.head_node: Optional[QuadNode] = None

    @classmethod
    def from_matrix(cls, matrix: List[List[bool]]) -> QuadLinkedList:

        # If the matrix rows aren't all equal, you can't logically create a Quad Linked List
        if not all(len(sub) == len(matrix[0]) for sub in matrix):
            raise ValueError("The matrix must be a square in order to be a valid QuadLinkedList")
        new_quad_list = cls()

        # Create the Header Nodes
        for i in range(len(matrix[0])):
            new_quad_list.__append_header(QuadNode(i))

        # Append the matrix elements
        for index, row in enumerate(matrix):
            for position, node in enumerate(row):
                if node:
                    new_quad_list.__add_node(position, QuadNode(index))
            new_quad_list.__fix_neighbors()

        return new_quad_list

    def __fix_neighbors(self):
        def __get_new_neighbors():
            head_node: QuadNode = self.head_node

            if head_node.top_node.right_node is None:
                yield head_node.top_node

            head_node = head_node.right_node
            while head_node is not self.head_node:
                if head_node.top_node.right_node is None:
                    yield head_node.top_node
                head_node = head_node.right_node

        neighbors = list(__get_new_neighbors())
        for index in range(len(neighbors)):
            neighbors[index].right_node = neighbors[(index + 1) % len(neighbors)]
            neighbors[index].left_node = neighbors[index - 1]

    def __append_header(self, node: QuadNode):
        """
        Create the QuadLinkedList header nodes. While maintaining the head node pointer position
        :param QuadNode node: The head node to be appended.
        :return:
        """
        if self.head_node is None:
            self.head_node = node
            self.head_node.left_node = node
            self.head_node.right_node = node
            self.head_node.top_node = node
            self.head_node.bottom_node = node
        else:
            self.head_node.left_node.right_node = node
            self.head_node.left_node.right_node.top_node = node
            self.head_node.left_node.right_node.bottom_node = node
            self.head_node.left_node.right_node.left_node = self.head_node.left_node
            self.head_node.left_node = node
            node.right_node = self.head_node

    def __add_node(self, header_column_position: int, new_node: QuadNode):
        def __get_header_node(position: int) -> QuadNode:
            head_node: QuadNode = self.head_node

            for _ in range(position):
                head_node = head_node.right_node

            return head_node

        column_node: QuadNode = __get_header_node(header_column_position)

        # Makes sure the new node is correctly inserted into the column node (in respect to the Top/Bottom nodes)
        column_node.top_node.bottom_node = new_node
        column_node.top_node.bottom_node.bottom_node = column_node
        column_node.top_node.bottom_node.top_node = column_node.top_node
        column_node.top_node = new_node


