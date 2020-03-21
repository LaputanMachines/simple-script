# coding=utf-8
"""Represents the Interpreter mechanism."""

from bin.constants import *
from bin.number import Number
from bin.runtime_result import RuntimeResult


class Interpreter:
    """The Interpreter mechanism for SimpleScript."""

    def visit(self, node, context):
        """
        Call the designated visit_ method given the Node.
        :param node: Node we wish to visit.
        :param context: Context of the caller.
        :return: The result of the visit_ method.
        """
        method_name = 'visit_{}'.format(type(node).__name__.lower())
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        """
        Handle unknown methods for visiting Nodes.
        :param node: Node we tried to visit.
        :param context: Context of the caller.
        """
        raise Exception('No visit_{} method defined.'.format(type(node).__name__.lower()))

    #####################################################
    # Names are all generated from all possible classes #
    # Forgive the odd naming convention, PEP8 Gods...   #
    #####################################################

    def visit_numbernode(self, node, context):
        """
        Returns the value of the Node as a Number.
        :param node: The Node with the numeric value.
        :param context: Context of the caller.
        :return: Number instance with the Node value.
        """
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_position(node.start_pos, node.end_pos))

    def visit_binopnode(self, node, context):
        """
        Returns the result of the binary operation.
        :param node: Node which houses two children Nodes.
        :param context: Context of the caller.
        :return: Result of the binary operation on both child Nodes.
        """
        result, error = None, None
        runtime_result = RuntimeResult()
        left_node = runtime_result.register(self.visit(node.left_node, context))
        right_node = runtime_result.register(self.visit(node.right_node, context))
        if runtime_result.error:
            return runtime_result
        if node.op_token.type == TP_PLUS:
            result, error = left_node.add_to(right_node)
        elif node.op_token.type == TP_MINUS:
            result, error = left_node.subtract_by(right_node)
        elif node.op_token.type == TP_POWER:
            result, error = left_node.power_by(right_node)
        elif node.op_token.type == TP_MUL:
            result, error = left_node.multiply_by(right_node)
        elif node.op_token.type == TP_DIV:
            result, error = left_node.divide_by(right_node)
        elif node.op_token.type == TP_MODULO:
            result, error = left_node.modulo_by(right_node)
        elif node.op_token.type == TP_CLEAN_DIV:
            result, error = left_node.divide_by(right_node, clean=True)
        if runtime_result.error:
            return runtime_result.failure(runtime_result)
        if error:
            return runtime_result.failure(error)
        return runtime_result.success(result.set_position(node.start_pos, node.end_pos))

    def visit_unaryopnode(self, node, context):
        """
        Returns result of the unary operator on the node.
        :param node: Node with which to perform a unary operation.
        :param context: Context of the caller.
        :return: Result of the unary operation on the node.
        """
        error = None
        runtime_result = RuntimeResult()
        number = runtime_result.register(self.visit(node.right_node, context))
        if runtime_result.error:
            return runtime_result
        if node.op_token.type == TP_MINUS:
            number, error = number.multiply_by(Number(-1))
        if error:
            return runtime_result.failure(error)
        return runtime_result.success(number.set_position(node.start_pos, node.end_pos))
