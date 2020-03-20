# coding=utf-8
"""
Source for the backend of the SimpleScript language.
Three main steps here: lexing, parsing, and interpreting.
Lexing transforms the string into tokens. Parsing turns
the tokens into an AST (abstract syntax tree). Interpreting
transforms executes the AST.
"""

from bin.context import Context
from bin.interpreter import Interpreter
from bin.lexer import Lexer
from bin.parser import Parser


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
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
