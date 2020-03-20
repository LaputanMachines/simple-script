# coding=utf-8
"""Source for the backend of the SimpleScript language."""

import constants
import errors


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


class Lexer:
    """The lexical analyzer component of the language."""

    def __init__(self, input_text):
        """
        Create instance of a Lexer.
        :param input_text: Input stream to parse using Lexer.
        """
        self.text = input_text
        self.position = -1
        self.current_character = None
        self.advance()  # 0-indexed array repr

    def advance(self):
        """Advance the position of the input stream."""
        self.position += 1
        self.current_character \
            = self.text[self.position] if self.position < len(self.text) else None

    def tokenize(self):
        """
        Tokenize the input text stream.
        :return: List of Token instances and/or Error instances.
        """
        tokens = []
        while self.current_character is not None:

            chars_to_skip = [' ', '\t']
            if self.current_character in chars_to_skip:
                self.advance()  # Skip useless chars

            # Transform input stream into a number Token
            elif self.current_character in constants.DIGITS:
                tokens.append(self.make_number())

            # Tokenize all valid operators
            elif self.current_character == '+':
                tokens.append(Token(constants.TP_PLUS))
                self.advance()
            elif self.current_character == '-':
                tokens.append(Token(constants.TP_MINUS))
                self.advance()
            elif self.current_character == '*':
                tokens.append(Token(constants.TP_MUL))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(constants.TP_DIV))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(constants.TP_LPAREN))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(constants.TP_RPAREN))
                self.advance()

            # Tokenize all remaining possible characters
            else:  # Report all illegal chars in stream
                illegal_character = self.current_character
                self.advance()  # Note: Advance to ensure pointer doesn't detach
                return [], errors.IllegalCharError('"' + illegal_character + '"')

        return tokens, None

    def make_number(self):
        """
        Turn text stream into either a float or an int Token.
        :return: Either a TP_FLOAT or a TP_INT number Token instance.
        """
        number_str, dot_count = '', 0
        while self.current_character is not None \
                and self.current_character in constants.DIGITS + '.':
            if self.current_character == '.':
                if dot_count == 1:
                    break  # Max one dot per float
                dot_count += 1
            number_str += self.current_character
            self.advance()
        if dot_count == 0:
            return Token(constants.TP_INT, int(number_str))
        else:  # Number must be a float
            return Token(constants.TP_FLOAT, float(number_str))


def run(stream):
    """
    Execute the Lexer on the text stream.
    :param stream: Input text stream to parse.
    :return: Stream of Token objects and Error messages.
    """
    lexer = Lexer(stream)
    tokens, error = lexer.tokenize()
    return tokens, error
