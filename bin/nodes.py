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
        self.start_pos = self.token.start_pos
        self.end_pos = self.token.end_pos

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
        self.start_pos = self.left_node.start_pos
        self.end_pos = self.right_node.end_pos

    def __repr__(self):
        return '({}, {}, {})'.format(self.left_node, self.op_token, self.right_node)


class UnaryOpNode:
    """Represents a Node for unary operations."""

    def __init__(self, op_token, right_node):
        """
        Initializes the unary operator.
        :param op_token: Operator Token for the unary operation.
        :param right_node: Node which has a unary operation.
        """
        self.op_token = op_token
        self.right_node = right_node
        self.start_pos = self.op_token.start_pos
        self.end_pos = self.right_node.end_pos

    def __repr__(self):
        return '({}, {})'.format(self.op_token, self.right_node)
