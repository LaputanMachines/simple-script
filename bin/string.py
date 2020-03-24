# coding=utf-8
"""Represents a String instance."""

from bin.number import Number
from bin.value import Value


class String(Value):
    """Represents a String instance."""

    def __init__(self, value):
        """
        Initializes a String instance.
        :param value: Value of the String.
        """
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return '{}'.format(self.value)

    def add_to(self, other):
        """
        Concatenate String instances together.
        :param other: Other String instance.
        :return: New concatenated String instance.
        """
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multiply_by(self, other):
        """
        Multiply a String by a Number instance.
        :param other: Number instance.
        :return: New String written out Number-times.
        """
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def is_true(self):
        """
        Returns TRUE if the String is non-empty.
        :return: TRUE if the String is non-empty.
        """
        return len(self.value) > 0

    def copy(self):
        """
        Makes a copy of the String instance.
        :return: A copy of the String instance.
        """
        copy = String(self.value)
        copy.set_position(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy
