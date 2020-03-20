# coding=utf-8
"""Represents Nodes in the backend of the SimpleScript language."""


class NumberNode:
    """Represents a Node of a number."""

    def __init__(self, token):
        """
        Initialize the number node.
        :param token: Token instance to use.
        """
        self.token = token

    def __repr__(self):
        return '{}'.format(self.token)


class BinOpNode:
    """Represents a Node for binary operations."""

    def __init__(self, left_node, op_token, right_node):
        """
        Initializes the binary operation node.
        :param left_node: Left node instance.
        :param op_token: Operator token instance.
        :param right_node: Right node instance.
        """
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return '({}, {}, {})'.format(self.left_node, self.op_token, self.right_node)
