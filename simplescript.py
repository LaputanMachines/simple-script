# coding=utf-8
"""
Source for the backend of the SimpleScript language.
Three main steps here: lexing, parsing, and interpreting.
Lexing transforms the string into tokens. Parsing turns
the tokens into an AST (abstract syntax tree). Interpreting
transforms executes the AST.
"""

import math
import os

from bin.context import Context
from bin.errors import ActiveRuntimeError
from bin.function import BaseFunction
from bin.interpreter import Interpreter
from bin.lexer import Lexer
from bin.list import List
from bin.number import Number
from bin.parser import Parser
from bin.runtime_result import RuntimeResult
from bin.string import String
from bin.symbol_table import SymbolTable

##############################
# DEFINE GLOBAL SYMBOL TABLE #
##############################

global_symbol_table = SymbolTable()

########################
# DEFINE ALL CONSTANTS #
########################

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)


################################################################
# BUILTIN FUNCTION CLASS                                       #
# DEFINED HERE BECAUSE IT CALLS THE RUN() FUNCTION             #
# WHICH RESULTS IN A CIRCULAR IMPORT IF PLACED IN ITS OWN FILE #
################################################################

class BuiltInFunction(BaseFunction):
    """Class of all built-in functions."""

    def __init__(self, name):
        """
        Initializes a BuiltInFunction instance.
        :param name: Name of the built-in function.
        """
        super().__init__(name)

    def __repr__(self):
        return '<built-in function {}>'.format(self.name)

    def execute(self, args):
        """
        Executes the BuiltInFunction instance.
        :param args: List of all arguments.
        :return: Value of whichever of the exec methods were called.
        """
        runtime_result = RuntimeResult()
        exec_context = self.generate_new_context()
        method_name = 'execute_{}'.format(self.name.lower())
        method = getattr(self, method_name, self.no_visit_method)
        runtime_result.register(self.check_and_populate_args(method.arg_names, args, exec_context))
        if runtime_result.error:
            return runtime_result
        return_value = runtime_result.register(method(exec_context))
        if runtime_result.error:
            return runtime_result
        return return_value

    def copy(self):
        """
        Makes a copy of a BuiltInFunction instance.
        :return: A BuiltInFunction instance.
        """
        builtin_copy = BuiltInFunction(self.name)
        builtin_copy.set_context(self.context)
        builtin_copy.set_position(self.start_pos, self.end_pos)
        return builtin_copy

    ##########################
    # ALL BUILT IN FUNCTIONS #
    # NAMES ARE GENERATED    #
    ##########################

    def no_visit_method(self, node, context):
        raise Exception('No "execute_{} method defined"'.format(self.name))

    def execute_print(self, exec_context):
        print(str(exec_context.symbol_table.get('value')))
        return RuntimeResult().success(Number(0))

    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_context):
        return RuntimeResult().success(String(str(exec_context.symbol_table.get('value'))))

    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_context):
        text = input()
        return RuntimeResult().success(String(text))

    execute_input.arg_names = []

    def execute_input_int(self, exec_context):
        while True:
            text = input()
            try:  # Try converting to int
                number = int(text)
                break
            except ValueError:
                print("'{}' must be an integer. Try again!".format(text))
        return RuntimeResult().success(Number(number))

    execute_input_int.arg_names = []

    def execute_clear(self, exec_context):
        os.system('cls' if os.name == 'nt' else 'cls')
        return RuntimeResult().success(Number(0))

    execute_clear.arg_names = []

    def execute_is_number(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), Number)
        return RuntimeResult().success(Number(1) if is_number else Number(0))

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), String)
        return RuntimeResult().success(Number(1) if is_number else Number(0))

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), List)
        return RuntimeResult().success(Number(1) if is_number else Number(0))

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), BaseFunction)
        return RuntimeResult().success(Number(1) if is_number else Number(0))

    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_context):
        list_ = exec_context.symbol_table.get("list")
        value = exec_context.symbol_table.get("value")
        if not isinstance(list_, List):
            return RuntimeResult().failure(ActiveRuntimeError(
                "First argument must be list",
                self.start_pos, self.end_pos,
                exec_context))
        list_.elements.append(value)
        return RuntimeResult().success(Number(0))

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_context):
        list_ = exec_context.symbol_table.get("list")
        index = exec_context.symbol_table.get("index")
        if not isinstance(list_, List):
            return RuntimeResult().failure(ActiveRuntimeError(
                "First argument must be list",
                self.start_pos, self.end_pos,
                exec_context))
        if not isinstance(index, Number):
            return RuntimeResult().failure(ActiveRuntimeError(
                "Second argument must be number",
                self.start_pos, self.end_pos,
                exec_context))
        try:  # Try pop() command in Python
            element = list_.elements.pop(index.value)
        except IndexError:
            return RuntimeResult().failure(ActiveRuntimeError(
                'Element at this index could not be removed from list because index is out of bounds',
                self.start_pos, self.end_pos,
                exec_context))
        return RuntimeResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_context):
        first_list = exec_context.symbol_table.get("first_list")
        end_list = exec_context.symbol_table.get("second_list")
        if not isinstance(first_list, List):
            return RuntimeResult().failure(ActiveRuntimeError(
                "First argument must be list",
                self.start_pos, self.end_pos,
                exec_context))
        if not isinstance(end_list, List):
            return RuntimeResult().failure(ActiveRuntimeError(
                "Second argument must be list",
                self.start_pos, self.end_pos,
                exec_context))
        first_list.elements.extend(end_list.elements)
        return RuntimeResult().success(Number(0))

    execute_extend.arg_names = ["first_list", "second_list"]

    def execute_len(self, exec_context):
        list_ = exec_context.symbol_table.get("list")
        if not isinstance(list_, List):
            return RuntimeResult().failure(ActiveRuntimeError(
                "Argument must be list",
                self.start_pos, self.end_pos,
                exec_context))
        return RuntimeResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

    def execute_run(self, exec_context):
        file_name = exec_context.symbol_table.get("fn")
        if not isinstance(file_name, String):
            return RuntimeResult().failure(ActiveRuntimeError(
                "Second argument must be string",
                self.start_pos, self.end_pos,
                exec_context))
        file_name = file_name.value
        try:
            with open(file_name, "r") as f:
                script = f.read()
        except Exception as exception:
            return RuntimeResult().failure(ActiveRuntimeError(
                "Failed to load script \"{}\"\n".format(file_name) + str(exception),
                self.start_pos, self.end_pos,
                exec_context))
        _, error = run(file_name, script)
        if error:
            return RuntimeResult().failure(ActiveRuntimeError(
                "Failed to finish executing script \"{}\"\n".format(file_name) + error.as_string(),
                self.start_pos, self.end_pos,
                exec_context))
        return RuntimeResult().success(Number(0))

    execute_run.arg_names = ["fn"]


#######################################
# EVERY BUILT IN FUNCTION  DEFINITION #
#######################################

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.print_ret = BuiltInFunction("print_ret")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.run = BuiltInFunction("run")

##############################################
# MAP ALL BUILT IN FUNCTIONS TO SYMBOL TABLE #
##############################################

global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("CLS", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUNC", BuiltInFunction.is_function)
global_symbol_table.set("APPEND", BuiltInFunction.append)
global_symbol_table.set("POP", BuiltInFunction.pop)
global_symbol_table.set("EXTEND", BuiltInFunction.extend)
global_symbol_table.set("LEN", BuiltInFunction.len)
global_symbol_table.set("RUN", BuiltInFunction.run)


##########################
# EXECUTE INTERPRETATION #
##########################

def run(fn, stream):
    """
    Execute the Lexer on the text stream.
    Three main steps here: lexing, parsing, and interpreting.
    Lexing transforms the string into tokens. Parsing turns
    the tokens into an AST (abstract syntax tree). Interpreting
    transforms executes the AST.
    :param fn: File name where stream originates.
    :param stream: Input text stream to parse.
    :return: Stream of Token objects and Error messages.
    """

    # Lex the input stream
    lexer = Lexer(stream, fn)
    tokens, error = lexer.tokenize()
    if error:  # Don't create the AST
        return None, error  # Tokenization failure

    # Parse the tokens
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Interpret the AST
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
