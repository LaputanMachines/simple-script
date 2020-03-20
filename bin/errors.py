# coding = utf-8
"""Error representations for the SimpleScript backend."""


class Error:
    """Custom error handling for language."""

    def __init__(self, error_name, error_details, pos_start, pos_end):
        """
        Create an Error instance with custom details.
        :param error_name: Name of the error instance.
        :param error_details: Description of the error.
        :param pos_start: Starting position of the character.
        :param pos_end: Ending position of the stream.
        """
        self.error_name = error_name
        self.error_details = error_details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        """Pretty-print error message."""
        error_msg = 'File {}, on line {}\n'.format(self.pos_start.fn, self.pos_start.ln + 1)
        error_msg += '{}: {}'.format(self.error_name, self.error_details)
        return error_msg


class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end):
        super(IllegalCharError, self).__init__(self.__class__.__name__,
                                               'Illegal character in the stream ({})'.format(details),
                                               pos_start,
                                               pos_end)
