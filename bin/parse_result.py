# coding=utf-8
"""Represents a ParseResult instance for operations."""


class ParseResult:
    """The result of parsed Tokens."""

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
        self.to_reverse_count = 0
        self.last_registered_advance_count = 0

    def register(self, result):
        """
        Registers the error of a parser operation and returns the Node.
        :param result: Result of the parsing of Tokens.
        :return: Node extracted from the ParseResult.
        """
        self.last_registered_advance_count = result.advance_count
        self.advance_count += result.advance_count
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node
        return result

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
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def try_register(self, result):
        """
        Tries to register a result instance.
        :param result: Current ParseResult instance.
        :return: The result of the register() call.
        """
        if result.error:
            self.to_reverse_count = result.advance_count
            return None  # Assume execution error
        return self.register(result)
