# coding=utf-8
"""All constants used in the backend of the SimpleScript language."""

from string import ascii_letters, digits

####################
# LIST OF KEYWORDS #
####################

KEYWORDS = [
    'VAR'
]

#################
# ALL CONSTANTS #
#################

DIGITS = digits
LETTERS = ascii_letters

##############
# ALL TOKENS #
##############

TP_IDENTIFIER = 'IDENTIFIER'
TP_KEYWORD = 'KEYWORD'
TP_EOF = 'EOF'

TP_INT = 'INT'
TP_FLOAT = 'FLOAT'
TP_PLUS = 'PLUS'
TP_MINUS = 'MINUS'
TP_MUL = 'MUL'
TP_DIV = 'DIV'
TP_CLEAN_DIV = 'CLEAN_DIV'
TP_MODULO = 'MODULO'
TP_POWER = 'POWER'
TP_EQUALS = 'EQ'
TP_LPAREN = 'LPAREN'
TP_RPAREN = 'RPAREN'
