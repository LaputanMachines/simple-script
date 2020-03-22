# coding=utf-8
"""Represents the Interpreter mechanism."""

from bin.constants import *
from bin.errors import ActiveRuntimeError
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
        elif node.op_token.type == TP_NE:
            result, error = left_node.get_comparison_ne(right_node)
        elif node.op_token.type == TP_EE:
            result, error = left_node.get_comparison_ee(right_node)
        elif node.op_token.type == TP_LT:
            result, error = left_node.get_comparison_lt(right_node)
        elif node.op_token.type == TP_LTE:
            result, error = left_node.get_comparison_lte(right_node)
        elif node.op_token.type == TP_GT:
            result, error = left_node.get_comparison_gt(right_node)
        elif node.op_token.type == TP_GTE:
            result, error = left_node.get_comparison_gte(right_node)
        elif node.op_token.matches(TP_KEYWORD, 'AND'):
            result, error = left_node.anded_by(right_node)
        elif node.op_token.matches(TP_KEYWORD, 'OR'):
            result, error = left_node.ored_by(right_node)
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
        elif node.op_token.matches(TP_KEYWORD, 'NOT'):
            number, error = number.notted()
        if error:
            return runtime_result.failure(error)
        return runtime_result.success(number.set_position(node.start_pos, node.end_pos))

    def visit_varaccessnode(self, node, context):
        """
        Accesses the value of variables in the stream.
        :param node: Node with which to fetch the variable.
        :param context: Context of the caller.
        :return: Value of fetching a variable's value and executing it.
        """
        runtime_result = RuntimeResult()
        var_name = node.var_name.value
        var_value = context.symbol_table.get(var_name)
        if not var_value:
            runtime_result.failure(ActiveRuntimeError('Variable name "{}" is not defined.'.format(var_name),
                                                      node.start_pos,
                                                      node.end_pos,
                                                      context))
        return runtime_result.success(var_value)

    def visit_varassignnode(self, node, context):
        """
        Assigns the value of variables in the stream.
        :param node: Node of a variable to assign.
        :param context: Context of the caller.
        :return: Value of the variable.
        """
        runtime_result = RuntimeResult()
        var_name = node.var_name.value
        var_value = runtime_result.register(self.visit(node.value_node, context))
        if runtime_result.error:
            return runtime_result
        context.symbol_table.set(var_name, var_value)
        return runtime_result.success(var_value)

    def visit_ifnode(self, node, context):
        """
        Accesses the IfNode instance in the stream.
        :param node: IfNode instance we wish to visit.
        :param context: Context of the caller.
        :return: Value of the if-statement, or None.
        """
        runtime_result = RuntimeResult()
        for condition, expr in node.cases:
            condition_value = runtime_result.register(self.visit(condition, context))
            if runtime_result.error:
                return runtime_result
            if condition_value.is_true():
                expr_value = runtime_result.register(self.visit(expr, context))
                if runtime_result.error:
                    return runtime_result
                return runtime_result.success(expr_value)
        if node.else_case:
            else_value = runtime_result.register(self.visit(node.else_case, context))
            if runtime_result.error:
                return runtime_result
            return runtime_result.success(else_value)
        return runtime_result.success(None)
