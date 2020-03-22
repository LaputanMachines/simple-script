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
        :return: Parser instance.
        """
        parser = self.expr()
        if not parser.error and self.current_token.type != TP_EOF:
            return parser.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                     self.current_token.end_pos,
                                                     'Expected "+", "-", "*", or "/" operator.'))
        return parser

    def atom(self):
        """
        Parses individual atoms in the stream.
        :return: The ParseResult instance.
        """
        parse_result = ParseResult()
        token = self.current_token

        # Parse integers and floating values
        if token.type in (TP_INT, TP_FLOAT):
            parse_result.register_advancement()
            self.advance()
            return parse_result.success(NumberNode(token))

        # Parse all possible identifiers
        elif token.type == TP_IDENTIFIER:
            parse_result.register_advancement()
            self.advance()
            return parse_result.success(VarAccessNode(token))

        # Parse all grouped expressions
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

        # Parse all if-statements
        elif token.matches(TP_KEYWORD, 'IF'):
            if_expr = parse_result.register(self.if_expr())
            if parse_result.error:
                return parse_result
            return parse_result.success(if_expr)

        # Defaults to raising an error
        # The InvalidSyntaxError will be raised if the Parser is
        # unable to properly parse the Token stream you provide
        return parse_result.failure(InvalidSyntaxError(
            "Expected int, float, identifier, '+', '-' or '(' in the expression.",
            token.start_pos, token.end_pos,
        ))

    def factor(self):
        """
        Implements the FACTOR grammar.
        :return: The Node of the numeral Token.
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

    def comparison_expr(self):
        """
        Implements the comparison expression grammar.
        :return: Node with the result of the comparison operation.
        """
        parse_result = ParseResult()
        if self.current_token.matches(TP_KEYWORD, 'NOT'):
            op_token = self.current_token
            parse_result.register_advancement()
            self.advance()
            node = parse_result.register(self.comparison_expr())
            if parse_result.error:
                return parse_result
            return parse_result.success(UnaryOpNode(op_token, node))
        node = parse_result.register(self.binary_operation(self.arithmetic_expr, [TP_EE,
                                                                                  TP_NE,
                                                                                  TP_LT,
                                                                                  TP_GT,
                                                                                  TP_LTE,
                                                                                  TP_GTE]))
        if parse_result.error:
            return parse_result.failure(InvalidSyntaxError(
                "Expected int, float, identifier, '+', '-', '(', or 'NOT' in the expression.",
                self.current_token.start_pos,
                self.current_token.end_pos))
        return parse_result.success(node)

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
        node = parse_result.register(self.binary_operation(self.comparison_expr,
                                                           [(TP_KEYWORD, 'AND'), (TP_KEYWORD, 'OR')]))
        if parse_result.error:
            return parse_result.failure(InvalidSyntaxError('Expected VAR or mathematical operator character.',
                                                           self.current_token.start_pos,
                                                           self.current_token.end_pos))
        return parse_result.success(node)

    def if_expr(self):
        """
        Implements the IF-EXPR grammar. Supports several cases
        as well as one final else case (optional).
        :return: IfNode containing all cases and an else case.
        """
        cases, else_case = [], None
        parse_result = ParseResult()
        if not self.current_token.matches(TP_KEYWORD, 'IF'):
            return parse_result.failure(InvalidSyntaxError('Expected an "IF" keyword.',
                                                           self.current_token.start_pos,
                                                           self.current_token.end_pos))
        parse_result.register_advancement()
        self.advance()
        condition = parse_result.register(self.expr())
        if parse_result.error:
            return parse_result
        if not self.current_token.matches(TP_KEYWORD, 'THEN'):
            return parse_result.failure(InvalidSyntaxError('Expected an "THEN" keyword.',
                                                           self.current_token.start_pos,
                                                           self.current_token.end_pos))
        parse_result.register_advancement()
        self.advance()
        expr = parse_result.register(self.expr())
        if parse_result.error:
            return parse_result
        cases.append((condition, expr))
        while self.current_token.matches(TP_KEYWORD, 'ELIF'):
            parse_result.register_advancement()
            self.advance()
            condition = parse_result.register(self.expr())
            if parse_result.error:
                return parse_result
            if not self.current_token.matches(TP_KEYWORD, 'THEN'):
                return parse_result.failure(InvalidSyntaxError('Expected an "THEN" keyword.',
                                                               self.current_token.start_pos,
                                                               self.current_token.end_pos))
            parse_result.register_advancement()
            self.advance()
            expr = parse_result.register(self.expr())
            if parse_result.error:
                return parse_result
            cases.append((condition, expr))
        if self.current_token.matches(TP_KEYWORD, 'ELSE'):
            parse_result.register_advancement()
            self.advance()
            else_case = parse_result.register(self.expr())
            if parse_result.error:
                return parse_result
        return parse_result.success(IfNode(cases, else_case))

    ################################
    # ALL BINARY OPERATION PARSERS #
    ################################

    def binary_operation(self, func_a, ops, func_b=None):
        """
        Generic binary operation handling for all
        multi-term grammars and their factors.
        :param func_a: Function which returns a factor.
        :param ops: Possible operations that can be handled.
        :param func_b: Optional second function.
        :return: Node of all possible TERM factors.
        """
        if not func_b:
            func_b = func_a
        parse_result = ParseResult()
        left_factor = parse_result.register(func_a())
        if parse_result.error:
            return parse_result

        # TODO (self.current_tok.type, self.current_tok.value) in ops

        while self.current_token.type in ops or self.current_token.type in ops:
            op_token = self.current_token
            parse_result.register_advancement()
            self.advance()
            right_factor = parse_result.register(func_b())
            if parse_result.error:
                return parse_result
            left_factor = BinOpNode(left_factor, op_token, right_factor)
        return parse_result.success(left_factor)

    def power(self):
        """
        Executes the power operation.
        :return: BinOpNode from the resulting operation.
        """
        return self.binary_operation(self.atom, [TP_POWER], self.factor)

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

    def arithmetic_expr(self):
        """
        Implements the grammar for the arithmetic expression.
        :return: Node of the result of the arithmetic expression.
        """
        return self.binary_operation(self.term, [TP_PLUS, TP_MINUS])
