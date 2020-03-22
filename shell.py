# coding=utf-8
"""Interactive shell for SimpleScript programming language"""

import simplescript

##################
# TERMINAL FLAGS #
##################

print_errors = False

###################
# WELCOME MESSAGE #
###################

hash_divider = '###################################################'
title_note = "# SimpleScript: Interpreted Programming Language  #"
copyright_note = "# (c) 2020 Michael Bassili Licensed Under GPL-3.0 #"
print('\n' + hash_divider + '\n' + title_note + '\n'
      + copyright_note + '\n' + hash_divider + '\n')

while True:
    input_stream = input('$ ')

    # Special terminal commands
    if input_stream == 'exit':
        print()  # Newline to separate content
        exit(0)  # Terminate from the shell
    elif input_stream == 'debug':
        print_errors = not print_errors
        continue

    result, error = simplescript.run('<stdin>', input_stream)
    if result:
        print(result)
    if error and print_errors:
        print(error)
