# coding = utf-8
"""Error representations for the SimpleScript backend."""


def string_with_arrows(text, pos_start, pos_end):
    """
    Prints incorrect string along with arrows pointing to issues.
    :param text: Text string which was illegal or incorrect.
    :param pos_start: Starting position for the error.
    :param pos_end: Ending position for the error
    :return: String with arrows pointing to incorrect text.
    """
    result = ''
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0:
        idx_end = len(text)

    # Calculate indices, generate string
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)
    return result.replace('\t', '')


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
        error_msg = '\nFile {}, on line {}\n'.format(self.pos_start.fn, self.pos_start.ln + 1)
        error_msg += '{}: {}'.format(self.error_name, self.error_details)
        error_msg += '\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) + '\n'
        return error_msg


class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end):
        super(IllegalCharError, self).__init__(self.__class__.__name__,
                                               'Illegal character in the stream ({})'.format(details),
                                               pos_start,
                                               pos_end)


class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end):
        super(InvalidSyntaxError, self).__init__(self.__class__.__name__,
                                                 'Invalid syntax in the stream ({})'.format(details),
                                                 pos_start,
                                                 pos_end)
