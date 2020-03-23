# coding=utf-8
"""Represents Value superclass instances."""

from bin.errors import ActiveRuntimeError


class Value:
    """Superclass of all possible values."""

    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.context = None
        self.set_pos()
        self.set_context()

    def set_pos(self, start_pos=None, end_pos=None):
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
