# coding=utf-8
"""Represents a ParseResult instance for operations."""


class ParseResult:
    """The result of parsed Tokens."""

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

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

    def register_advancement(self):
        self.advance_count += 1
