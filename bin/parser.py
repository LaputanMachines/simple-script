# coding=utf-8
"""
Represents the Parser mechanism for Nodes.
Every parsing function corresponds to a grammar
for the BASIC language (and by extension the
SimpleScript language too).
"""

from bin.constants import *
from bin.errors import InvalidSyntaxError
from bin.nodes import *
from bin.parse_result import ParseResult


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
        Triggers the parsing of the input stream.
        :return: ParseResult instance.
        """
        parse_result = self.expr()
        if not parse_result.error and self.current_token.type != TP_EOF:
            return parse_result.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                           self.current_token.end_pos,
                                                           'Expected "+", "-", "*", or "/" operator.'))
        return parse_result

    def atom(self):
        """
        Parses individual atoms in the stream.
        :return: The ParseResult instance.
        """
        parse_result = ParseResult()
        token = self.current_token
        if token.type in (TP_INT, TP_FLOAT):
            parse_result.register_advancement()
            self.advance()
            return parse_result.success(NumberNode(token))
        elif token.type == TP_IDENTIFIER:
            parse_result.register_advancement()
            self.advance()
            return parse_result.success(VarAccessNode(token))
        elif token.type == TP_LPAREN:
            parse_result.register_advancement()
            self.advance()
            expression = parse_result.register(self.expr())
            if parse_result.error:
                return parse_result
            if self.current_token.type == TP_RPAREN:
                parse_result.register_advancement()
                self.advance()
                return parse_result.success(expression)
            else:
                return parse_result.failure(InvalidSyntaxError(
                    'Expected ")" in expression.',
                    self.current_token.start_pos,
                    self.current_token.end_pos))

        return parse_result.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int, float, identifier, '+', '-' or '('"
        ))

    def power(self):
        """
        Executes the power operation.
        :return: BinOpNode from the resulting operation.
        """
        return self.binary_operation(self.atom, [TP_POWER], self.factor)

    def factor(self):
        """
        Implements the FACTOR grammar.
        :return: The ParseResult of the numeral Token.
        """
        token = self.current_token
        parse_result = ParseResult()
        if token.type in [TP_PLUS, TP_MINUS]:
            parse_result.register_advancement()
            self.advance()
            factor = parse_result.register(self.factor())
            if parse_result.error:
                return parse_result
            return parse_result.success(UnaryOpNode(token, factor))

        return self.power()

    def binary_operation(self, func_a, ops, func_b=None):
        """
        Generic binary operation handling for all
        multi-term grammars and their factors.
        :param func_a: Function which returns a factor.
        :param ops: Possible operations that can be handled.
        :param func_b: Optional second function.
        :return: ParseResult of all possible TERM factors.
        """
        if not func_b:
            func_b = func_a
        parse_result = ParseResult()
        left_factor = parse_result.register(func_a())
        if parse_result.error:
            return parse_result
        while self.current_token.type in ops:
            op_token = self.current_token
            parse_result.register(self.advance())
            right_factor = parse_result.register(func_b())
            if parse_result.error:
                return parse_result
            left_factor = BinOpNode(left_factor, op_token, right_factor)
        return parse_result.success(left_factor)

    def term(self):
        """
        Implements the TERM grammar.
        :return: BinOpNode of all possible FACTOR objects.
        """
        return self.binary_operation(self.factor, [TP_MUL,
                                                   TP_DIV,
                                                   TP_POWER,
                                                   TP_CLEAN_DIV,
                                                   TP_MODULO])

    def expr(self):
        """
        Implements the EXPR grammar for variables.
        :return: BinOpNode of all possible TERM objects.
        """
        parse_result = ParseResult()
        if self.current_token.matches(TP_KEYWORD, 'VAR'):
            parse_result.register(self.advance())
            if self.current_token.type != TP_IDENTIFIER:
                return parse_result.failure(InvalidSyntaxError('Expected identifier in the expression.',
                                                               self.current_token.start_pos,
                                                               self.current_token.end_pos))
            var_name = self.current_token
            parse_result.register(self.advance())
            if self.current_token.type != TP_EQUALS:
                return parse_result.failure(InvalidSyntaxError('Expected "=" character in the expression.',
                                                               self.current_token.start_pos,
                                                               self.current_token.end_pos))
            parse_result.register(self.advance())
            expression = parse_result.register(self.expr())
            if parse_result.error:
                return parse_result
            return parse_result.success(VarAssignNode(var_name, expression))
        return self.binary_operation(self.term, [TP_PLUS, TP_MINUS])
