# coding=utf-8
"""
Represents Function, and other similar instances.
Note: The Function() class definition is implemented in
      'interpreter.py' because it's execute() function requires the
      interpreter. Importing the Interpreter() class would
      result in a circular import, something which Python despises.
"""

from bin.context import Context
from bin.errors import ActiveRuntimeError
from bin.runtime_result import RuntimeResult
from bin.symbol_table import SymbolTable
from bin.value import Value


#############################################################
# FUNCTION CLASS DEFINITION                                 #
# PLACED HERE BECAUSE EXECUTE() FUNC USES INTERPRETER       #
# IMPLEMENTING THIS ELSEWHERE RESULTS IN CIRCULAR IMPORT    #
#############################################################

class BaseFunction(Value):
    """Represents a basic built-in."""

    def __init__(self, name):
        """
        Initializes the BaseFunction class.
        :param name:
        """
        super().__init__()
        self.name = name or '<anonymous>'

    def generate_new_context(self):
        """
        Generates a new Context instance.
        :return: Context instance that was created.
        """
        context = Context(self.name, self.context, self.start_pos)
        context.symbol_table = SymbolTable(context.parent_context.symbol_table)
        return context

    def check_args(self, arg_names, args):
        """
        Checks that correct number of args are present.
        :param arg_names: List of argument names.
        :param args: List of arguments passed into func.
        :return: None, if there are no issues.
        """
        runtime_result = RuntimeResult()
        if len(args) > len(arg_names):
            return runtime_result.failure(ActiveRuntimeError(
                'Too many arguments'.format(len(args) - len(arg_names)),
                self.start_pos,
                self.end_pos,
                self.context))
        if len(args) < len(arg_names):
            return runtime_result.failure(ActiveRuntimeError(
                'Too few arguments'.format(len(arg_names) - len(args)),
                self.start_pos,
                self.end_pos,
                self.context))
        return runtime_result.success(None)

    @staticmethod
    def populate_args(arg_names, args, exec_context):
        """
        Populates the args for a given Context.
        :param arg_names: Name of all args.
        :param args: List of all arg values.
        :param exec_context: Context to update.
        """
        for index in range(len(args)):
            arg_name = arg_names[index]
            arg_value = args[index]
            arg_value.set_context(exec_context)
            exec_context.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_context):
        """
        Checks args before populating the Context.
        :param arg_names: Names of all args.
        :param args: Values of all args.
        :param exec_context: Context we wish to update.
        :return: None, if there are no issues.
        """
        runtime_result = RuntimeResult()
        runtime_result.register(self.check_args(arg_names, args))
        if runtime_result.error:
            return runtime_result
        self.populate_args(arg_names, args, exec_context)
        return runtime_result.success(None)
