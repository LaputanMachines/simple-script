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


class VarAccessNode:
    """Supports accessing the variables in the grammar."""

    def __init__(self, var_name):
        """
        Initializes a VarAccessNode instance.
        :param var_name: Name of the VAR Token.
        """
        self.var_name = var_name
        self.start_pos = self.var_name.start_pos
        self.end_pos = self.var_name.end_pos


class VarAssignNode:
    """Supports assigning values to variables in the grammar."""

    def __init__(self, var_name, value_node):
        """
        Initializes a VarAssignNode instance.
        :param var_name: Name of the VAR object.
        :param value_node: Node value of the object.
        """
        self.var_name = var_name
        self.value_node = value_node
        self.start_pos = self.var_name.start_pos
        self.end_pos = self.value_node.end_pos


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


class IfNode:
    """Represents a Node for if-statements."""

    def __init__(self, cases, else_case):
        """
        Initializes an IfNode with cases and an else case.
        :param cases: List of all cases in the if-statement.
        :param else_case: Optional else case in the if-statement.
        """
        self.cases = cases
        self.else_case = else_case
        self.start_pos = self.cases[0][0].start_pos
        self.end_pos = (self.else_case if self.else_case
                        else self.cases[len(self.cases) - 1][0]).end_pos


class ForNode:
    """Represents a Node for for-loops."""

    def __init__(self, var_name_token, start_value_node, end_value_node, step_value_node, body_node):
        """
        Initializes a ForNode for-loop statement.
        :param var_name_token: Name of the variable Token.
        :param start_value_node: When to begin the iteration.
        :param end_value_node: When to end the iteration.
        :param step_value_node: Value of each step in the loop.
        :param body_node: What gets evaluated on every iteration.
        """
        self.var_name_token = var_name_token
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.start_pos = self.var_name_token.start_pos
        self.end_pos = self.body_node.end_pos


class WhileNode:
    """Represents a Node for while-loops."""

    def __init__(self, condition, body_node):
        """
        Initializes a WhileNode for while loops.
        :param condition: Condition with which to continue execution.
        :param body_node: What gets evaluated on every execution.
        """
        self.condition = condition
        self.body_node = body_node
        self.start_pos = self.condition.start_pos
        self.end_pos = self.body_node.end_pos


class FuncDefNode:
    """Represents a function definition."""

    def __init__(self, var_name_token, arg_name_tokens, body_node):
        """
        Initializes a FuncDefNode for functions in stream.
        :param var_name_token: Name of the function to create.
        :param arg_name_tokens: Argument Tokens for the function.
        :param body_node: Expression assigned to new function.
        """
        self.var_name_token = var_name_token
        self.arg_name_tokens = arg_name_tokens
        self.body_node = body_node
        self.start_pos = None
        if self.var_name_token:
            self.start_pos = self.var_name_token.start_pos
        elif len(self.arg_name_tokens) > 0:
            self.start_pos = self.arg_name_tokens[0].start_pos
        else:  # Assume no arguments or variable names
            self.start_pos = self.body_node.start_pos
        self.end_pos = self.body_node.end_pos


class CallNode:
    """Represents a call to a function"""

    def __init__(self, node_to_call, arg_nodes):
        """
        Initializes a CallNode for calling functions.
        :param node_to_call: Node of the function to call.
        :param arg_nodes: Arguments for the function.
        """
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
        self.start_pos = self.node_to_call.start_pos
        self.end_pos = None
        if len(self.arg_nodes) > 0:
            self.end_pos = self.arg_nodes[len(self.arg_nodes) - 1].end_pos
        else:  # Assume function has no arguments to call
            self.end_pos = self.node_to_call.end_pos


class ListNode:
    """Represents a list."""

    def __init__(self, element_nodes, start_pos, end_pos):
        """
        Initializes a ListNode for lists.
        :param element_nodes: Element Nodes in the list.
        :param start_pos: Starting Position instance.
        :param end_pos: Ending Position instance.
        """
        self.element_nodes = element_nodes
        self.start_pos = start_pos
        self.end_pos = end_pos
