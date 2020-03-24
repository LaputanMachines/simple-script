# SimpleScript Programming Language

SimpleScript is an interpreted, BACIC-like programming language built with Python. It is small, clean, and powerful. 
The language itself is straightforward and allows for cleaner-looking mathematical operations and data processing.

## Installation

Ensure Python 3 is installed on your system. SimpleScript does not use any external libraries.
This makes it entirely portable since it does not require the installation of any third-party libraries. **TL;DR: all you need is Python 3 installed on your system.** Nothing else is needed to write and execute SimpleScript programs.

## How To Use

You can use Python to launch the interactive shell. This will allow you to play with the SimpleSCript language in your terminal. You can use the shell to test expressions. 
In your BASH terminal, run the `shell.py` script using Python. 

```BASH
$ python shell.py 
```

By default, error messages are not displayed. To toggle the visibility of error messages, use the `debug` command.
This will allow all error messages to be printed after any interpretation. This is handy for improving the language itself. It's also handy to see smaller syntax and execution errors that the interpreter may have encountered.
The reason it's not enabled by default is that one of the principles of SimpleScript is to rarely stop you dead in your tracks. Error handling measures have been built to inform-if-needed, otherwise it will attempt to sally forth.

```BASIC
$ DEBUG
DEBUG MODE IS ON

$ DEBUG
DEBUG MODE IS OFF
```

To exit the interactive shell, simply use the `exit` keyword. This will terminate your program and perform garbage collection.
You'll be dumped back into the BASH terminal you launched from. 

```BASIC
$ EXIT
```

More specifically, garbage collection of the variables and functions you created and used will occur. All system variables and functions will return to their original state.
This means that if you overrode the system variable `FALSE` to the value `10`, for example, that it would be restored back to its default value of `0`.

## Special Variables

The following special variables have set values in the language. However, they _can_ be remapped in your program. This is by design and allows your program to define its own basic terms and concepts.

| Variable | SimpleScript Variable | Value | Use |
| --- | --- | --- | --- |
| Null/NaN | `NULL` | 0 | Represents an empty value |
| Logical True | `TRUE` | 1 | Represents a True Boolean | 
| Logical False | `FALSE` | 0 | Represents a False Boolean | 

Note that since these values are stored in a symbol table, you can also define `true` as your own version of `TRUE`; the values of `TRUE` and `true` can be different if you want. SimpleScript will never tell you that you shouldn't reassign these special variables. Configure your program as you'd like.

## Supported Math Operators

Here is a table including all supported mathematical operations in SimpleScript. Most are similar to Python or BASIC's implementations, but I've made some small changes which hopefully improve the look and feel of larger mathematical expressions.

| Operation | SimpleScript Command | Description | Notes |
|---|---|---|---|
| Addition | `+` | Performs addition |  |
| Subtraction | `-` | Performs subtraction |  |
| Multiplication | `*` | Performs multiplication |  |
| Division | `/` | Performs typical floating division | Cannot divide by 0 |
| Integer Division | `|` | Performs division using integers | Cannot divide by 0 |
| Power | `^` | Raises expression to a power | Supports negative powers |
| Modulo | `%` | Returns remainder of division |  |

All these operations can be performed on both numeric values and sub-expressions, including variables. Variables are executed before any other numeric operation, so you can actually assign variables _while performing numeric operations_ on other values. 

## Examples Of Math Operations

Basic arithmetic operations can be performed directly on numbers, variables, and other values. Mathematical operations all return their associated value. Anytime a floating point operation is introduced, the data type returned will be a float. 

```BASIC
$ (2 + 1) | (4 - 1)
1
```

```BASIC
$ 10 % 5
 0
```

```BASIC
$ 1 + 2 - 3 * 4 / 5
0.6000000000000001
```

```BASIC
$ ((1 + 2) * 3 ^ 2) / 2
13.5
```

```BASIC
$ 10 | 2 + (8 ^ 2) - 6
63
```

As you'd expect, division by zero is not allowed. If you try, the interpreter will inform you that the operation you're trying to execute is invalid. It will even highlight the error in your file. Negative powers are valid operations that will evaluate to the same result as would a similar BASIC operation.

```BASIC
$ 12345 / 0

Traceback (most recent call last):
File <stdin>, line 1, in <program>
File <stdin>, on line 1
12345 / 0
        ^
```

```BASIC
$ 98765 / (4 - 5 + 1)

Traceback (most recent call last):
File <stdin>, line 1, in <program>
File <stdin>, on line 1
98765 / (4 - 5 + 1)
         ^^^^^^^^^
```

Operations that eventually evaluate into zero are also not allowed, as seen in the above example. In this case, the entire sub-expression is highlighted by the interpreter. This hopefully provides enough tracing and error information to fix the issue in your program. The stack trace will always be displayed in error messages.e," there is a great deal that can be improved upon. I, for one, am less-than-satisfied with much of the variable and function mechanisms of SimpleScript.

## Variables

Variables can be declared by using the `VAR` keyword. Variable names can include letters and underscores in their name. Variables can be re-assigned without restriction. Variables are stored in a symbol table, so they can be mutated and altered throughout execution.

```BASIC
$ VAR my_variable = 12345
12345
$ my_variable
12345
```

```BASIC
$ VAR my_other_variable = 67890
67890
$ my_other_variable
67890
```

```BASIC
$ VAR addition = my_variable + my_other_variable
80235
$ addition
80235
```

Also, variables can be assigned _in the middle of expressions_ which may seem odd to those used to assigning variables before use. However, this can allow one to spawn helper variables in context to one statement instead of having to add to the parent's scope.

```BASIC
$ VAR x = 10 + (VAR y = 5)   
15
$ y
5
```

This kind of inline assignment is thanks to the interpretation of the abstract syntax tree (AST). Instead of searching line-by-line for variables to be assigned, SimpleScript simply treats the `VAR` keyword like a token that triggers the parsing of its sub-tree. In short, SimpleScript considers `VAR` definitions a higher priority than brackets in the BEDMAS order of operations.

## Lists

SimpleScript allows for lists to be defined. They are immutable, unlike Python lists. 
You can define a list, add elements to a list, remove elements from a list, and join two lists together.
Since lists are immutable, you'll need to leverage list joins and value extraction to obtain your resulting list. 

```BASIC
$ VAR list = [1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
```

```BASIC 
$ VAR list = [1, 2, 3]
[1, 2, 3]
list + [4, 5]
[1, 2, 3, 4, 5]
```

```BASIC
$ VAR list = [1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
$ VAR other_list = [6, 7, 8, 9, 0]
[6, 7, 8, 9, 0]
$ list * other_list
[1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
```

```BASIC
$ VAR list = [1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
$ list - 1
[1, 3, 4, 5]
$ list - 0
[3, 4, 5]
$ list - (-1)
[3, 4]
```

You can get elements by-index in lists using the `/` operator. You can also use negative index values to fetch values from the ends of arrays. 
As always, you can chain expressions together. For example, you can evaluate an expression that results in an index for the list. 

```BASIC
$ [1, 2, 3, 4, 5] / 0
1
```

```BASIC
$ VAR list = [1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
$ list / -1
5
```

Lists are useful in performing computations on data. For example, images can be expressed as arrays of integers. 
Using SimpleScript, you can use this list representation to perform computations on the image by interacting with its respective list.

## Strings

Strings are essentially just lists of individual characters. In SimpleScript, you can define and operate on strings the same way you would in BASIC. 
You can concatenate two or more strings together, and you can repeat strings by multiplying it with a number.

```BASIC
$ "This is a string!"
This is a string!
```

```BASIC
$ "I can start here, " + "and end here!"
I can start here, and end here!
```

```BASIC
$ "Echo! " * 5
Echo! Echo! Echo! Echo! Echo! 
```

```BASIC
$ FUNC welcome (name, repeat) -> "Welcome, " * repeat + name
<function welcome>
$ welcome ("Michael", 5)
Welcome, Welcome, Welcome, Welcome, Welcome, Michael
```

You can set variables to equal strings and you can also write anonymous functions which perform actions on strings.

## Supported Comparison Operators

The following comparison operators are supported in SimpleScript. They can be used in addition to variable assignment and function executions. This is due to how the interpreter understands the ASTs being generated. The result is that you can chain together long and complex comparisons without needing to stop to define anything.

| Operator | SimpleScript Command | Description |
| --- | --- | --- |
| Exactly Equals | `==` | Evaluates to TRUE if both sides are equal |
| Not Equals | `!=` | Evaluates to TRUE if both sides are not equal |
| Less Than | `<` | Evaluates to TRUE if the left side is smaller than the right side |
| Greater Than | `>` | Evaluates to TRUE if the left side is larger than the right side |
| Less Than Or Equals To | `<=` | Evaluates to TRUE if the left side is smaller or equal to the right side |
| Greater Than Or Equals To | `>=` | Evaluates to TRUE if the left side is larger or equal to the right side |

These operators are the same as BASIC or Python's operators, so their syntax should hopefully be familiar to some. Comparisons between 1 and 0 can be interpreted as comparisons between TRUE and FALSE respectively.

## Supported Logical Operators

No language would be complete without logical operators. These operate the same way as logic gates do. All of AND, OR, and NOT operate in the same way they do in regular BASIC and Python.

| Operator | SimpleScript Command | Description | Notes |
| --- | --- | --- | --- | 
| Logical AND | `AND` | Evaluates to TRUE if both sizes are TRUE |  |
| Logical OR | `OR` | Evaluates to TRUE if at least one side is TRUE |  |
| Negation | `NOT` | Evaluates to the opposite Boolean value of the expression | TRUE becomes FALSE, and vice-versa |

These can be chained into variable definitions and other assignments and function declarations to evaluate the truth values of abstract statements. The underlying ASTs of these operations are built in such a way to be able to handle applications on abstract entities; you can apply these logical operators to any expression.

## If-Statements

You can make if-statements by using the `IF`, `ELSE`, and `ELIF` keywords. Pairing this with logical or comparison operators can allow for dynamic variable assignment.

```BASIC
$ IF TRUE THEN 123
123
```

```BASIC
$ IF (1 + 2) <= (3 + 4) THEN TRUE
1
```

```BASIC
$ IF 1 != 1 THEN 100 
$ IF 1 != 1 THEN 100 ELSE 999
999
```

```BASIC
$ IF TRUE == 0 THEN (VAR x = 9) ELIF TRUE == 1 THEN (VAR x = 5) ELSE (VAR x = 0)
5
```

```BASIC
$ IF (10 - 5) == 5 THEN (VAR x = TRUE) ELSE (VAR x = FALSE)
1
$ x
1
```

These control flow operations also allow for the inline assignment of variables, as seen above. In the case that no value is assigned (e.g. `IF 0 THEN 123`), then no value is outputted.

## For-Loops

For-loops are control flows that execute a set number of times before terminating. For-loops are great for iteration and compounding operations.
SimpleScript follows the BASIC model of for-loops, where a loop condition are defined and a body expression is grouped up and executed. More simply, SimpleScript for-loops are formatted like for-loops in C.

```BASIC
$ FOR i = 1 TO 10 THEN 2 ^ i
[2, 4, 8, 16, 32, 64, 128, 256, 512]
```

```BASIC
$ VAR x = 1
1
$ FOR i = 1 TO 5 THEN VAR x = x + i
[2, 4, 7, 11]
$ x
11
```

```BASIC
$ VAR y = 100
100
$ FOR i = 100 TO 0 STEP -1 THEN VAR y = y - i
[0, -99, ... -4949, -4950]
$ y
-4950
```

```BASIC
$ VAR z = 1  
1
$ IF 10 == (20 - 10) THEN FOR i = 0 TO 10 THEN VAR z = z + i
[1, 2, 4, 7, 11, 16, 22, 29, 37, 46]
$ z
46
```

SimpleScript allows you to assign variables inline with your for-loop. This opens up the possibility for dynamic variable assignment depending on predefined contexts.
The greatest benefit, however, is that because SimpleScript allows for mutations of variables, you can initialize a variable beforehand and then use it to perform meta-computations in the for-loop itself. 

## While-Loops

Like for-loops, while-loops take some condition and execute an expression. The difference here is that the provided expression will keep executing until the provided condition proves false. 
This allows us to repeat programs and expressions until we reach some desired goal. 

```BASIC
$ VAR x = 1
1
$ WHILE x < 10 THEN VAR x = x + 1
[2, 3, 4, 5, 6, 7, 8, 9, 10]
$ x
10
```

```BASIC
$ VAR y = 10
10
$ WHILE y > 0 AND (TRUE == 1) THEN VAR y = y - 2
[8, 6, 4, 2, 0]
$ y
0
```

Variables and sub-expressions can be chained together to form large compound conditions for your while-loop. The body of the loop can be similarly built. 
These larger compound control flow programs can chain into function calls and other sub-routines, making them very powerful.

## Functions

You can use the `FUNC` keyword to create functions in SimpleScript. Like Python, you can assign functions to variables for future use. Function names can be made up of letters and underscores. 

```BASIC
$ FUNC my_math (a, b, c) -> a + b - c
<function my_math>
$ my_math (1, 2, 3)    
0
```

```BASIC
$ VAR my_func = FUNC my_math (a, b, c) -> a + b - c
<function my_math>
$ my_func
<function my_math>
$ my_func (1, 2, 3)  
0
$ my_math (1, 2, 3)    
0
```

```BASIC
$ debug
$ FUNC bad_func (a, b) -> a | b ^ 2
<function bad_func>
$ bad_func ()

Traceback (most recent call last):
File <stdin>, line 1, in <program>
bad_func ()
^^^^^^^^
```

```BASIC
$ debug
$ FUNC bad_func (a, b) -> a | b
<function bad_func>
$ bad_func (1, 2, 3, 4)

Traceback (most recent call last):
File <stdin>, line 1, in <program>
bad_func (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^
```

If `debug` is enabled, the interpreter will complain if you add too many or too few function parameters. You can also create anonymous functions (e.g. lambda functions in Python) using similar syntax.

```BASIC
$ FUNC (a, b) -> a ^ 2 + b ^ 2
<function <anonymous>>
$ VAR anon_func = FUNC (a, b) -> a ^ 2 + b ^ 2
<function <anonymous>>
$ anon_func (2, 3)  
13
```

Like variables and flow control loops, you can chain together large compound function calls inside smaller anonymous function declarations. 
The interpreter's backend has been built to handle abstract layers of expressions and nesting; there is no restriction to the number of nested compound functions you can use.

---

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

This grammar was lifted from [davidcallanan/py-myopl-code](https://github.com/davidcallanan/py-myopl-code/blob/master/ep14/grammar.txt) as they already had the most accurate and feature-rich BASIC grammar I could find online. This grammar is completely barebones; all BASIC implementations would be identical. This was lifted to save me the hastle of drafting the initial grammar myself, a task reserved for POWs and grammar enthusiasts.

## Backend Architecture

The process of building and interpreting a programming language from scratch can be split into three main components. Each component produces their own deliverable that is used as an input for the following process.

- Lexing: Turns text strings into a list of tokens
- Parsing: Turns the list of tokens into an abstract syntax tree (AST)
- Interpreting: Evaluates every node of the AST to return a result

The three components are named accordingly in the `bin/` directory. They are: `lexer.py`, `parser.py`, and `interpreter.py`. These three components are the backbone of (most) programming languages.

## Related Readings

Here are some of the best physical and digital resources I could find on the subject of creating an interpreter for a programming language from scratch:

* [Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages (Pragmatic Programmers)](https://www.amazon.ca/gp/product/193435645X/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=193435645X&linkCode=as2&tag=russblo0b-20&linkId=MP4DCXDV6DJMEJBL)
* [Writing Compilers and Interpreters: A Software Engineering Approach](https://www.amazon.ca/gp/product/0470177071/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0470177071&linkCode=as2&tag=russblo0b-20&linkId=UCLGQTPIYSWYKRRM)
* [Modern Compiler Implementation in Java](https://www.amazon.ca/gp/product/052182060X/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=052182060X&linkCode=as2&tag=russblo0b-20&linkId=ZSKKZMV7YWR22NMW)
* [Modern Compiler Design](https://www.amazon.com/gp/product/1461446988/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1461446988&linkCode=as2&tag=russblo0b-20&linkId=PAXWJP5WCPZ7RKRD)
* [Compilers: Principles, Techniques, and Tools (2nd Edition)](https://www.amazon.ca/gp/product/0321486811/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321486811&linkCode=as2&tag=russblo0b-20&linkId=GOEGDQG4HIHU56FQ)
* [The "Let’s Build A Simple Interpreter" Blog Series](https://ruslanspivak.com/lsbasi-part1/)
* [The "Make YOUR OWN Programming Language" Video Series](https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)
* [Introduction to Programming Languages/Interpreted Programs](https://en.wikibooks.org/wiki/Introduction_to_Programming_Languages/Interpreted_Programs)
* [Clean Architecture: A Craftsman's Guide to Software Structure and Design (Robert C. Martin Series)](https://www.amazon.ca/dp/B075LRM681?ref_=cm_sw_r_kb_dp_zbbTDb7E1P022&tag=davidcallanan-20&linkCode=kpe)

Hopefully these help inform similar projects in the future. While SimpleScript is "complete," there is a great deal that can be improved upon. I, for one, am less-than-satisfied with much of the variable and function mechanisms of SimpleScript.
