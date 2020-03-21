# coding=utf-8
"""
Represents the Parser mechanism for Nodes.
Every parsing function corresponds to a grammar
for the BASIC language (and by extension the
SimpleScript language too).
"""

from bin.constants import *
from bin.errors import InvalidSyntaxError
from bin.nodes import NumberNode, BinOpNode, UnaryOpNode


class Parser:
    """Represents the Parser object for Nodes."""

    def __init__(self, tokens):
        """
        Initializes the Parser instance.
        :param tokens: Tokens to be parsed by the Parser.
        """
        self.tokens = tokens
        self.token_idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        """
        Advance the Token index.
        :return: Current Token instance.
        """
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token

    def parse(self):
        """

        :return:
        """
        parse_result = self.expr()
        if not parse_result.error and self.current_token.type != TP_EOF:
            return parse_result.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                           self.current_token.end_pos,
                                                           'Expected "+", "-", "*", or "/" operator.'))
        return parse_result

    def factor(self):
        """
        Implements the FACTOR grammar.
        :return: The ParseResult of the numeral Token.
        """
        parse_result = ParseResult()
        token = self.current_token
        if token.type in [TP_PLUS, TP_MINUS]:
            parse_result.register(self.advance())
            factor = parse_result.register(self.factor())
            if parse_result.error:
                return parse_result
            return parse_result.success(UnaryOpNode(token, factor))
        elif token.type in [TP_INT, TP_FLOAT]:
            parse_result.register(self.advance())
            return parse_result.success(NumberNode(token))
        elif token.type == TP_LPAREN:
            parse_result.register(self.advance())
            expression = parse_result.register(self.expr())
            if parse_result.error:
                return parse_result
            if self.current_token.type == TP_RPAREN:
                parse_result.register(self.advance())
                return parse_result.success(expression)
            return parse_result.failure(InvalidSyntaxError('Expected ")" character.',
                                                           self.current_token.start_pos,
                                                           self.current_token.end_pos))
        return parse_result.failure(
            InvalidSyntaxError('Expected INT or FLOAT value.',
                               token.start_pos,
                               token.end_pos))

    def binary_operation(self, func, ops):
        """
        Generic binary operation handling for all
        multi-term grammars and their factors.
        :param func: Function which returns a factor.
        :param ops: Possible operations that can be handled.
        :return: ParseResult of all possible TERM factors.
        """
        parse_result = ParseResult()
        left_factor = parse_result.register(func())
        if parse_result.error:
            return parse_result
        while self.current_token.type in ops:
            op_token = self.current_token
            parse_result.register(self.advance())
            right_factor = parse_result.register(func())
            if parse_result.error:
                return parse_result
            left_factor = BinOpNode(left_factor, op_token, right_factor)
        return parse_result.success(left_factor)

    def term(self):
        """
        Implements the TERM grammar.
        :return: BinOpNode of all possible FACTOR objects.
        """
        return self.binary_operation(self.factor, [TP_MUL, TP_DIV, TP_POWER, TP_CLEAN_DIV, TP_MODULO])

    def expr(self):
        """
        Implements the EXPR grammar.
        :return: BinOpNode of all possible TERM objects.
        """
        return self.binary_operation(self.term, [TP_PLUS, TP_MINUS])


class ParseResult:
    """The result of parsed Tokens."""

    def __init__(self):
        self.error = None
        self.node = None

    def register(self, result):
        """
        Registers the error of a parser operation and returns the Node.
        :param result: Result of the parsing of Tokens.
        :return: Node extracted from the ParseResult.
        """
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node
        return result  # Already a Node

    def success(self, node):
        """
        Stores the value of the Node instance and returns a ParseResult.
        :param node: Node of the successful parse operation.
        :return: ParseResult with the stored Node value.
        """
        self.node = node
        return self

    def failure(self, error):
        """
        Store the value of an Error instance in the ParseResult.
        :param error: An Error instance.
        :return: The Error raised in the parse operation.
        """
        self.error = error
        return self
