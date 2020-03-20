# coding=utf-8
"""Keeps track of stack traces in runtime environment."""


class Context:
    """Keeps track of stack traces in runtime environment."""

    def __init__(self, display_name, parent_context=None, parent_entry_pos=None):
        """
        Initializes a new Context instance with parents and positions.
        :param display_name: Name of the Context to be displayed.
        :param parent_context: Parent Context instance.
        :param parent_entry_pos: Position of the parent Context instance.
        """
        self.display_name = display_name
        self.parent_context = parent_context
        self.parent_entry_pos = parent_entry_pos
