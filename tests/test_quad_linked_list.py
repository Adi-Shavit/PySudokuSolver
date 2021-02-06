from src.quad_linked_list import QuadLinkedList


def test_quad_linked_list_from_matrix_method_creates_valid_quad_list():
    matrix = [[False, True, False, True, False, True],
              [True, False, True, False, True, False],
              [False, False, True, True, False, False],
              [True, False, False, False, False, True]]

    ql = QuadLinkedList.from_matrix(matrix)

    assert ql.head_node.right_node.bottom_node.right_node is ql.head_node.right_node.right_node.right_node.bottom_node
    assert ql.head_node.right_node.bottom_node.right_node.top_node is ql.head_node.right_node.right_node.right_node
    assert ql.head_node.right_node.top_node.left_node is ql.head_node.left_node.top_node


def test_quad_linked_list_edges_are_circular():
    ql = QuadLinkedList.from_matrix([[True, False]])
    assert ql.head_node.right_node.right_node is ql.head_node.left_node

    assert ql.head_node.left_node.top_node is ql.head_node.left_node.bottom_node is ql.head_node.left_node

    assert ql.head_node.right_node.bottom_node is ql.head_node.right_node.top_node is not ql.head_node
    assert ql.head_node.right_node.bottom_node.bottom_node is ql.head_node.right_node
    assert ql.head_node.right_node.bottom_node is ql.head_node.right_node.top_node

    assert ql.head_node.header_node is ql.head_node
    assert ql.head_node.right_node.header_node is ql.head_node.right_node
