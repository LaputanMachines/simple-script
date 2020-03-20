# coding=utf-8
"""Source for the Token representation."""


class Token:
    """Generic Tokens in the language."""

    def __init__(self, token_type, token_value=None):
        """
        Create Token instance with value and type.
        :param token_type: Type of the Token being created.
        :param token_value: Optional value of the Token.
        """
        self.type = token_type
        self.value = token_value

    def __repr__(self):
        if self.value:
            return '{}:{}'.format(self.type, self.value)
        return '{}'.format(self.type)
