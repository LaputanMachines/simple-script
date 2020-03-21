# coding=utf-8
"""All helper methods that do not belong to any module."""


def string_with_arrows(text, start_pos, end_pos):
    """
    Prints incorrect string along with arrows pointing to issues.
    :param text: Text string which was illegal or incorrect.
    :param start_pos: Starting position for the error.
    :param end_pos: Ending position for the error
    :return: String with arrows pointing to incorrect text.
    """
    result = ''
    idx_start = max(text.rfind('\n', 0, start_pos.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0:
        idx_end = len(text)

    # Calculate indices, generate string
    line_count = end_pos.ln - start_pos.ln + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = start_pos.col if i == 0 else 0
        col_end = end_pos.col if i == line_count - 1 else len(line) - 1
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)
    return result.replace('\t', '')
