# coding=utf-8
"""Represents a Tokenizer of Tokens."""

from bin.constants import *
from bin.errors import IllegalCharError
from bin.position import Position
from bin.token import Token


class Lexer:
    """The lexical analyzer component of the language."""

    def __init__(self, input_text, fn):
        """
        Create instance of a Lexer.
        :param input_text: Input stream to parse using Lexer.
        :param fn: File name of the document.
        """
        self.text = input_text
        self.position = Position(-1, 0, -1, fn, input_text)
        self.current_character = None
        self.advance()  # 0-indexed array repr
        self.fn = fn

    def advance(self):
        """Advance the position of the input stream."""
        self.position.advance(self.current_character)
        self.current_character \
            = self.text[self.position.idx] if self.position.idx < len(self.text) else None

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
            elif self.current_character in DIGITS:
                tokens.append(self.make_number())

            # Tokenize all valid operators
            elif self.current_character == '+':
                tokens.append(Token(TP_PLUS, start_pos=self.position))
                self.advance()
            elif self.current_character == '-':
                tokens.append(Token(TP_MINUS, start_pos=self.position))
                self.advance()
            elif self.current_character == '*':
                tokens.append(Token(TP_MUL, start_pos=self.position))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(TP_DIV, start_pos=self.position))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TP_LPAREN, start_pos=self.position))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TP_RPAREN, start_pos=self.position))
                self.advance()

            # Tokenize all remaining possible characters
            else:  # Report all illegal chars in stream
                start_pos = self.position.copy()
                illegal_character = self.current_character
                self.advance()  # Note: Advance to ensure pointer doesn't detach
                return [], IllegalCharError('"' + illegal_character + '"', start_pos, self.position)

        # Mark end with EOF and return
        tokens.append(Token(TP_EOF))
        return tokens, None

    def make_number(self):
        """
        Turn text stream into either a float or an int Token.
        :return: Either a TP_FLOAT or a TP_INT number Token instance.
        """
        number_str, dot_count = '', 0
        start_pos = self.position.copy()
        while self.current_character is not None \
                and self.current_character in DIGITS + '.':
            if self.current_character == '.':
                if dot_count == 1:
                    break  # Max one dot per float
                dot_count += 1
            number_str += self.current_character
            self.advance()

        # Tokenize the numeric value to INT or FLOAT types
        if dot_count == 0:  # Tokenize an INT data type
            return Token(TP_INT, int(number_str), start_pos, self.position)
        else:  # Must be FLOAT data type
            return Token(TP_FLOAT, float(number_str), start_pos, self.position)
