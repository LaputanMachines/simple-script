# coding=utf-8
"""Source for the backend of the SimpleScript language."""

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
    return tokens, error
