# coding=utf-8
"""Represents Numbers in the context of SimpleScript."""

from bin.errors import ActiveRuntimeError


class Number:
    """Represents a Number instance in the interpreter."""

    def __init__(self, value):
        """
        Initialize a Number instance with a value.
        Note that we initialize context and positions to None so
        that Python's interpreter doesn't complain of unresolved
        class-level variables.
        :param value: Value of the new Number instance.
        """
        self.value = value
        self.start_pos = None
        self.end_pos = None
        self.set_position()
        self.context = None
        self.set_context()

    def __repr__(self):
        return str(self.value)

    def set_position(self, start_pos=None, end_pos=None):
        """
        Set the position of the number in the context of the AST.
        :param start_pos: Starting position in the stream.
        :param end_pos: Ending position in the stream.
        :return: Self instance of Number with new positions.
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def add_to(self, other):
        """
        Add two Number values together.
        No possible errors can occur for addition between Numbers.
        :param other: Number instance.
        :return: Number instance with the summed value.
        """
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtract_by(self, other):
        """
        Subtract two Number values together.
        No possible errors can occur for subtraction between Numbers.
        :param other: Number instance.
        :return: Number instance with the subtracted value.
        """
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiply_by(self, other):
        """
        Multiply two Number values together.
        No possible errors can occur for multiplication between Numbers.
        :param other: Number instance.
        :return: Number instance with the multiplied value.
        """
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divide_by(self, other):
        """
        Divide two Number values together.
        :param other: Number instance.
        :return: Number instance with the divided value.
        """
        if isinstance(other, Number):
            if other.value == 0:
                return None, ActiveRuntimeError('Division by 0 is not allowed.',
                                                other.start_pos,
                                                other.end_pos,
                                                self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def set_context(self, context=None):
        """
        Sets the class-level context to be a Context instance.
        :param context: Context instance to be set.
        """
        self.context = context
        return self
