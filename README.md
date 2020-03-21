# SimpleScript: Interpreted Programming Language

  * [Installation](#installation)
  * [How To Use](#how-to-use)
  * [Language Grammars](#language-grammars)
  * [Backend Architecture](#backend-architecture)

Interpreted programming language built with Python. 
Docs and releases are served through GitHub. 
It's turing complete and is simple to use.
It is based on the BASIC programming language, and features error highlighting, variables, functions, etc.
The language is simple to use yet robust enough to support the creation of actual programs.

## Installation

Ensure Python 3 is installed on your system. SimpleScript does not use any external libraries.
This makes it entirely portable since it does not require the installation of any third-party libraries.

## How To Use

You can use Python to launch the interactive shell. This will allow you to play with the SimpleSCript language in your terminal. You can use the shell to test expressions. 
In your BASH terminal, run the `shell.py` script using Python. 

```BASH
python shell.py  # Launches the interactive SimpleScript shell
```

## Language Grammars

The SimpleScript language is built around the grammar of BASIC. The grammar was used in the creation of the Lexer and the Parser. It served to inform the design and development of the creation of the abstract syntax trees and their tokens.

```text
statements  : NEWLINE* statement (NEWLINE+ statement)* NEWLINE*

statement		: KEYWORD:RETURN expr?
						: KEYWORD:CONTINUE
						: KEYWORD:BREAK
						: expr

expr        : KEYWORD:VAR IDENTIFIER EQ expr
            : comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*

comp-expr   : NOT comp-expr
            : arith-expr ((EE|LT|GT|LTE|GTE) arith-expr)*

arith-expr  :	term ((PLUS|MINUS) term)*

term        : factor ((MUL|DIV) factor)*

factor      : (PLUS|MINUS) factor
            : power

power       : call (POW factor)*

call        : atom (LPAREN (expr (COMMA expr)*)? RPAREN)?

atom        : INT|FLOAT|STRING|IDENTIFIER
            : LPAREN expr RPAREN
            : list-expr
            : if-expr
            : for-expr
            : while-expr
            : func-def

list-expr   : LSQUARE (expr (COMMA expr)*)? RSQUARE

if-expr     : KEYWORD:IF expr KEYWORD:THEN
              (statement if-expr-b|if-expr-c?)
            | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)

if-expr-b   : KEYWORD:ELIF expr KEYWORD:THEN
              (statement if-expr-b|if-expr-c?)
            | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)

if-expr-c   : KEYWORD:ELSE
              statement
            | (NEWLINE statements KEYWORD:END)

for-expr    : KEYWORD:FOR IDENTIFIER EQ expr KEYWORD:TO expr 
              (KEYWORD:STEP expr)? KEYWORD:THEN
              statement
            | (NEWLINE statements KEYWORD:END)

while-expr  : KEYWORD:WHILE expr KEYWORD:THEN
              statement
            | (NEWLINE statements KEYWORD:END)

func-def    : KEYWORD:FUN IDENTIFIER?
              LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN
              (ARROW expr)
            | (NEWLINE statements KEYWORD:END)
```

## Backend Architecture

TODO

---

<img src="https://img.shields.io/badge/license-GNU-red.svg" /> <img src="https://img.shields.io/badge/maintainer-FlatlanderWoman-informational.svg" /> <img src="https://img.shields.io/badge/version-1.0-yellow.svg" />
