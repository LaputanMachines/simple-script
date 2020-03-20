# coding = utf-8
"""Error representations for the SimpleScript backend."""


class Error:
    """Custom error handling for language."""

    def __init__(self, error_name, error_details):
        """
        Create an Error instance with custom details.
        :param error_name: Name of the error instance.
        :param error_details: Description of the error.
        """
        self.error_name = error_name
        self.error_details = error_details

    def __repr__(self):
        """Pretty-print error message."""
        return '{}: {}'.format(self.error_name, self.error_details)


class IllegalCharError(Error):
    def __init__(self, details):
        super(IllegalCharError, self).__init__(self.__class__.__name__,
                                               'Illegal character in the stream ({})'.format(details))
