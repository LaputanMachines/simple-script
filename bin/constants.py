# coding=utf-8
"""All constants used in the backend of the SimpleScript language."""

import operator
from string import ascii_letters, digits

#############
# OPERATORS #
#############

operations = {'>': operator.gt,
              '<': operator.lt,
              '>=': operator.ge,
              '<=': operator.le,
              '==': operator.eq,
              '!=': operator.ne,
              'AND': operator.and_,
              'OR': operator.or_}

####################
# LIST OF KEYWORDS #
####################

TP_IDENTIFIER = 'IDENTIFIER'
TP_KEYWORD = 'KEYWORD'
TP_EOF = 'EOF'
KEYWORDS = [
    'VAR',
    'AND',
    'OR',
    'NOT',
    'IF',
    'THEN',
    'ELIF',
    'ELSE',
    'FOR',
    'TO',
    'STEP',
    'WHILE',
    'FUNC'
]

#################
# ALL CONSTANTS #
#################

DIGITS = digits
LETTERS = ascii_letters

##################
# ALL DATA TYPES #
##################

TP_INT = 'INT'
TP_FLOAT = 'FLOAT'
TP_STRING = 'STRING'

#############
# ALL MATHS #
#############

TP_PLUS = 'PLUS'
TP_MINUS = 'MINUS'
TP_MUL = 'MUL'
TP_DIV = 'DIV'
TP_CLEAN_DIV = 'CLEAN_DIV'
TP_MODULO = 'MODULO'
TP_POWER = 'POWER'
TP_EQUALS = 'EQ'
TP_COMMA = 'COMMA'
TP_ARROW = 'ARROW'

###############
# COMPARISONS #
###############

TP_EE = 'EE'
TP_NE = 'NE'
TP_LT = 'LT'
TP_GT = 'GT'
TP_LTE = 'LTE'
TP_GTE = 'GTE'

#################
# ALL GROUPINGS #
#################

TP_LPAREN = 'LPAREN'
TP_RPAREN = 'RPAREN'
TP_LSQUARE = 'LSQUARE'
TP_RSQUARE = 'RSQUARE'
