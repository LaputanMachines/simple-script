# coding=utf-8
"""Represents Value superclass instances."""

from bin.errors import ActiveRuntimeError
from bin.runtime_result import RuntimeResult


class Value:
    """Superclass of all possible values."""

    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.context = None
        self.set_position()
        self.set_context()

    def set_position(self, start_pos=None, end_pos=None):
        """
        Sets the position values for a Value instance.
        :param start_pos: Starting position.
        :param end_pos: Ending position.
        :return: Value instance with new positions.
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def set_context(self, context=None):
        """
        Sets the context of the Value instance.
        :param context: Context of the instance.
        :return: Value instance with the set context.
        """
        self.context = context
        return self

    def illegal_operation(self, other=None):
        """
        Processes illegal operations against Values.
        :param other: Other values being acted on.
        :return: RuntimeError with illegal operands.
        """
        if not other:
            other = self
        return ActiveRuntimeError('Illegal operation performed',
                                  self.start_pos,
                                  other.end_pos,
                                  self.context)

    #######################################
    # DEFAULT FUNCTIONS                   #
    # CHILD CLASSES SHOULD OVERRIDE THESE #
    #######################################

    def add_to(self, other):
        return None, self.illegal_operation(other)

    def subtract_by(self, other):
        return None, self.illegal_operation(other)

    def multiply_by(self, other):
        return None, self.illegal_operation(other)

    def divide_by(self, other):
        return None, self.illegal_operation(other)

    def power_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RuntimeResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False
