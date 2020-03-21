# SimpleScript: Interpreted Programming Language

Interpreted programming language built with Python. 
Docs and releases are served through GitHub. 
It's turing complete and is simple to use.
It is based on the BASIC programming language, and features error highlighting, variables, functions, etc.
The language is simple to use yet robust enough to support the creation of actual programs.

---

  * [Installation](#installation)
  * [How To Use](#how-to-use)
  * [Language Grammars](#language-grammars)
  * [Backend Architecture](#backend-architecture)

---

## Installation

Ensure Python 3 is installed on your system. SimpleScript does not use any external libraries.
This makes it entirely portable since it does not require the installation of any third-party libraries. **TL;DR: all you need is Python 3 installed on your system.** Nothing else is needed to write and execute SimpleScript programs.

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

The process of building and interpreting a programming language from scratch can be split into three main components. Each component produces their own deliverable that is used as an input for the following process.

- Lexing: Turns text strings into a list of tokens
- Parsing: Turns the list of tokens into an abstract syntax tree (AST)
- Interpreting: Evaluates every node of the AST to return a result

The three components are named accordingly in the `bin/` directory. They are: `lexer.py`, `parser.py`, and `interpreter.py`. These three components are the backbone of (most) programming languages.`

---

<img src="https://img.shields.io/badge/license-GNU-red.svg" /> <img src="https://img.shields.io/badge/maintainer-FlatlanderWoman-informational.svg" /> <img src="https://img.shields.io/badge/version-v1.0-yellow.svg" />
