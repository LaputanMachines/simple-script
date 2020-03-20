# coding=utf-8
"""Source for the backend of the SimpleScript language."""

from bin.parser import Parser
from bin.tokenizer import Lexer


def run(fn, stream):
    """
    Execute the Lexer on the text stream.
    :param fn: File name where stream originates.
    :param stream: Input text stream to parse.
    :return: Stream of Token objects and Error messages.
    """
    lexer = Lexer(stream, fn)
    tokens, error = lexer.tokenize()
    if error:  # Don't create the AST
        return None, error  # Tokenization failure

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
