# coding=utf-8
"""Represents the Interpreter mechanism."""

from bin.constants import *
from bin.context import Context
from bin.errors import ActiveRuntimeError
from bin.number import Number
from bin.runtime_result import RuntimeResult
from bin.symbol_table import SymbolTable
from bin.value import Value


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
            runtime_result.failure(ActiveRuntimeError('VAR "{}" not defined'.format(var_name),
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

    def visit_fornode(self, node, context):
        """
        Visits the ForNode for for-loops in the stream.
        :param node: Node of the for-loop.
        :param context: Context of the caller.
        :return: None for success.
        """
        runtime_result = RuntimeResult()
        start_value = runtime_result.register(self.visit(node.start_value_node, context))
        if runtime_result.error:
            return runtime_result
        end_value = runtime_result.register(self.visit(node.end_value_node, context))
        if runtime_result.error:
            return runtime_result
        if node.step_value_node:
            step_value = runtime_result.register(self.visit(node.step_value_node, context))
            if runtime_result.error:
                return runtime_result
        else:  # Default to one iteration
            step_value = Number(1)

        # Note: PEP 8 doesn't allow for lambda expressions to be assigned to
        #       variables directly. They prefer a function definition. However, this
        #       is the cleanest way to do this. Code is read more often than it's
        #       written. This expression is easier to read and understand as an
        #       inline lambda assignment.
        index = start_value.value
        if step_value.value >= 0:
            condition = lambda: index < end_value.value
        else:  # Step value must be negative
            condition = lambda: index > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_token.value, Number(index))
            index += step_value.value
            runtime_result.register(self.visit(node.body_node, context))
            if runtime_result.error:
                return runtime_result
        return runtime_result.success(None)

    def visit_whilenode(self, node, context):
        """
        Visits the WhileNode for while-loops in the stream.
        :param node: Node of the while-loop.
        :param context: Context of the caller.
        :return: None for success.
        """
        runtime_result = RuntimeResult()
        while True:
            condition = runtime_result.register(self.visit(node.condition, context))
            if runtime_result.error:
                return runtime_result
            if not condition.is_true():
                break
            runtime_result.register(self.visit(node.body_node, context))
            if runtime_result.error:
                return runtime_result
        return runtime_result.success(None)

    def visit_funcdefnode(self, node, context):
        """
        Visits a FuncDefNode instance.
        :param node: The FuncDefNode instance.
        :param context: The caller's context.
        :return: Function Node instance.
        """
        runtime_result = RuntimeResult()
        func_name = node.var_name_token.value if node.var_name_token else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_node = Function(func_name, body_node, arg_names). \
            set_context(context).set_pos(node.start_pos, node.end_pos)
        if node.var_name_token:
            context.symbol_table.set(func_name, func_node)
        return runtime_result.success(func_node)

    def visit_callnode(self, node, context):
        """
        Visits the CallNode instance.
        :param node: The CallNode instance.
        :param context: The caller's context.
        :return: The resulting Node from the exec call.
        """
        args = []
        runtime_result = RuntimeResult()
        value_to_call = runtime_result.register(self.visit(node.node_to_call, context))
        if runtime_result.error:
            return runtime_result
        value_to_call = value_to_call.copy().set_pos(node.start_pos, node.end_pos)
        for arg_node in node.arg_nodes:
            args.append(runtime_result.register(self.visit(arg_node, context)))
            if runtime_result.error:
                return runtime_result
        return_value = runtime_result.register(value_to_call.execute(args))
        if runtime_result.error:
            return runtime_result
        return runtime_result.success(return_value)


##########################################################
# FUNCTION CLASS DEFINITION                              #
# PLACED HERE BECAUSE EXEC() FUNC USES INTERPRETER       #
# IMPLEMENTING THIS ELSEWHERE RESULTS IN CIRCULAR IMPORT #
##########################################################

class Function(Value):
    """Represents a Function instance."""

    def __init__(self, name, body_node, arg_names):
        """
        Initializes a Function instance.
        :param name: Name of the function.
        :param body_node: Body Node instance of the function.
        :param arg_names: Argument names for the function.
        """
        super().__init__()
        self.name = name or '<anonymous>'
        self.body_node = body_node
        self.arg_names = arg_names

    def __repr__(self):
        return '<function {}>'.format(self.name)

    def execute(self, args):
        """
        Execute a Function instance.
        :param args: Arguments being passed into the Function.
        :return: Value of the executed Function.
        """
        runtime_result = RuntimeResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.start_pos)
        new_context.symbol_table = SymbolTable(new_context.parent_context.symbol_table)
        if len(args) > len(self.arg_names):
            return runtime_result.failure(ActiveRuntimeError(
                'Too many arguments'.format(len(args) - len(self.arg_names)),
                self.start_pos,
                self.end_pos,
                self.context))
        if len(args) < len(self.arg_names):
            return runtime_result.failure(ActiveRuntimeError(
                'Too few arguments'.format(len(self.arg_names) - len(args)),
                self.start_pos,
                self.end_pos,
                self.context))
        for index in range(len(args)):
            arg_name = self.arg_names[index]
            arg_value = args[index]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)
        value = runtime_result.register(interpreter.visit(self.body_node, new_context))
        if runtime_result.error:
            return runtime_result
        return runtime_result.success(value)

    def copy(self):
        """
        Copies a Function instance.
        :return: A new Function instance.
        """
        function_copy = Function(self.name, self.body_node, self.arg_names)
        function_copy.set_context(self.context)
        function_copy.set_pos(self.start_pos, self.end_pos)
        return function_copy
