# coding=utf-8
"""Source for the Token representation."""


class Token:
    """Generic Tokens in the language."""

    def __init__(self, token_type, token_value=None, start_pos=None, end_pos=None):
        """
        Create Token instance with value and type.
        :param token_type: Type of the Token being created.
        :param token_value: Optional value of the Token.
        """
        self.type = token_type
        self.value = token_value
        if start_pos:
            self.start_pos = start_pos.copy()
            self.end_pos = start_pos.copy()
            self.end_pos.advance()
        if end_pos:
            self.end_pos = end_pos.copy()

    def __repr__(self):
        if self.value:
            return '{}:{}'.format(self.type, self.value)
        return '{}'.format(self.type)

    def matches(self, token_type, token_value):
        """
        Returns True if the type and value of two Tokens matches.
        :param token_type: Type of the Token instance.
        :param token_value: Value of the Token instance.
        :return: True if the type and value of two Token instances match.
        """
        return self.type == token_type and self.value == token_value
