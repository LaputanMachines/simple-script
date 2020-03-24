# coding=utf-8
"""
Source for the backend of the SimpleScript language.
Three main steps here: lexing, parsing, and interpreting.
Lexing transforms the string into tokens. Parsing turns
the tokens into an AST (abstract syntax tree). Interpreting
transforms executes the AST.
"""

import math

from bin.built_in_function import BuiltInFunction
from bin.context import Context
from bin.interpreter import Interpreter
from bin.lexer import Lexer
from bin.number import Number
from bin.parser import Parser
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
