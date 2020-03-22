# coding=utf-8
"""Represents Numbers in the context of SimpleScript."""

from bin.constants import operations
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

    def power_by(self, other):
        """
        Raise two Number values together.
        No possible errors can occur for power operations between Numbers.
        :param other: Number instance.
        :return: Number instance with the multiplied value.
        """
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def modulo_by(self, other):
        """
        Takes modulo of two Number values.
        :param other: Number instance.
        :return: Number instance with the modulo remainder value.
        """
        if isinstance(other, Number):
            if other.value == 0:
                return None, ActiveRuntimeError('Division by 0 is not allowed.',
                                                other.start_pos,
                                                other.end_pos,
                                                self.context)
            return Number(self.value % other.value).set_context(self.context), None

    def divide_by(self, other, clean=False):
        """
        Divide two Number values together.
        :param other: Number instance.
        :param clean: True to perform a clean division.
        :return: Number instance with the divided value.
        """
        if isinstance(other, Number):
            if other.value == 0:
                return None, ActiveRuntimeError('Division by 0 is not allowed.',
                                                other.start_pos,
                                                other.end_pos,
                                                self.context)
            if clean:  # Perform integer division
                return Number(self.value // other.value).set_context(self.context), None
            else:  # Perform regular floating point division
                return Number(self.value / other.value).set_context(self.context), None

    def set_context(self, context=None):
        """
        Sets the class-level context to be a Context instance.
        :param context: Context instance to be set.
        """
        self.context = context
        return self

    def is_true(self):
        """
        Returns True if the value of the Number is not 0.
        :return: True if the value is not 0 (i.e. not False).
        """
        return self.value != 0

    ###############################
    # ALL LOGICAL OPERATIONS      #
    # EVERY FUNCTION IS IDENTICAL #
    ###############################

    def apply_comparison(self, other, op_str):
        """
        Applies the comparison operator to the other Number.
        Call the int() function to convert our output
        to either a 1 (TRUE) or 0 (FALSE) result.
        :param other: Other Number to apply the operation to.
        :param op_str: The string of the operator of the operation we desire.
        :return: Number with the resulting operation.
        """
        return Number(int(operations[op_str](self.value, other.value))).set_context(self.context), None

    def get_comparison_ee(self, other):
        return self.apply_comparison(other, '==')

    def get_comparison_ne(self, other):
        return self.apply_comparison(other, '!=')

    def get_comparison_lt(self, other):
        return self.apply_comparison(other, '<')

    def get_comparison_lte(self, other):
        return self.apply_comparison(other, '<=')

    def get_comparison_gt(self, other):
        return self.apply_comparison(other, '>')

    def get_comparison_gte(self, other):
        return self.apply_comparison(other, '>=')

    def anded_by(self, other):
        return self.apply_comparison(other, 'AND')

    def ored_by(self, other):
        return self.apply_comparison(other, 'OR')

    def notted(self):
        """
        Negates the provided boolean value, turning it
        into a Node. Only unique comparison.
        :return: Number node with the negated value.
        """
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
