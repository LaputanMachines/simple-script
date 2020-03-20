# coding=utf-8
"""Represents the position of text in the shell."""


class Position:
    """Represents the position of streamed text."""

    def __init__(self, idx, ln, col, fn, ftxt):
        """
        Initialize the Position instance.
        :param idx: Index of the stream.
        :param ln: Line number of the stream.
        :param col: Column number of the stream.
        :param fn: Name of the current file.
        :param ftxt: Text in the current file.
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        """
        Advance the position of the stream.
        :param current_char: Current char in the stream.
        """
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        """
        Deep-copy the Position instance.
        New Position instance is made and stored whenever an illegal
        character is encountered. This is so that the error can be more
        easily traceable (this will, however expend more memory).
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
