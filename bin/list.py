# coding=utf-8
"""Represents a List value."""

from bin.errors import ActiveRuntimeError
from bin.number import Number
from bin.value import Value


class List(Value):
    """Represents a List value."""

    def __init__(self, elements):
        """
        Initializes a List instance.
        :param elements: Elements of the List.
        """
        super().__init__()
        self.elements = elements

    def __repr__(self):
        # Note: Usually I use the format() function for formatting strings
        #       but in this case, the harder-to-read f'' method is actually
        #       faster. Unfortunately, this makes things harder to understand.
        return f'[{", ".join([str(element) for element in self.elements])}]'

    def add_to(self, other):
        """
        Add to the List instance.
        :param other: Element instance to add.
        :return: New List instance with added value.
        """
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subtract_by(self, other):
        """
        Subtract value from List.
        :param other: Index of the value to extract.
        :return: New List instance without desired index value.
        """
        if isinstance(other, Number):
            new_list = self.copy()
            try:  # Try pop() call on the list()
                new_list.elements.pop(other.value)
                return new_list, None
            except IndexError:  # Catch Python's attempt at pop()
                return None, ActiveRuntimeError('Index not found',
                                                self.start_pos,
                                                other.end_pos,
                                                self.context)
        else:  # Index of List value must be a Number
            return ActiveRuntimeError('Illegal operation performed',
                                      self.start_pos,
                                      other.end_pos,
                                      self.context)

    def multiply_by(self, other):
        """
        Join to List instances together.
        :param other: Another List instance.
        :return: The resulting List from the join operation.
        """
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:  # Cannot join List to any other data type
            return ActiveRuntimeError('Illegal operation performed',
                                      self.start_pos,
                                      other.end_pos,
                                      self.context)

    def divide_by(self, other):
        """
        Get value from the List instance.
        :param other: Index of value to fetch from List.
        :return: Value requested from the List.
        """
        if isinstance(other, Number):
            try:  # Try indexing on the list()
                return self.elements[other.value], None
            except IndexError:  # Catch Python's attempt at pop()
                return None, ActiveRuntimeError('Index not found',
                                                self.start_pos,
                                                other.end_pos,
                                                self.context)
        else:  # Index of List value must be a Number
            return ActiveRuntimeError('Illegal operation performed',
                                      self.start_pos,
                                      other.end_pos,
                                      self.context)

    def copy(self):
        """
        Returns a copy of the List instance.
        :return: Copy of List current instance.
        """
        new_list = List(self.elements[:])
        new_list.set_position(self.start_pos, self.end_pos)
        new_list.set_context(self.context)
        return new_list
