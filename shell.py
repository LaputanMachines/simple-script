# coding=utf-8
"""Interactive shell for SimpleScript programming language"""

import simplescript

hash_divider = '###################################################'
title_note = "# SimpleScript: Interpreted Programming Language  #"
copyright_note = "# (c) 2020 Michael Bassili Licensed Under GPL-3.0 #"
print('\n' + hash_divider + '\n' + title_note + '\n'
      + copyright_note + '\n' + hash_divider + '\n')

while True:
    input_stream = input('$ ')
    if input_stream == 'exit':
        print()  # Newline to separate content
        exit(0)  # Terminate from the shell
    result, error = simplescript.run('<stdin>', input_stream)
    output_stream = error if error else result
    print(output_stream)
