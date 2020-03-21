SimpleScript supports all essential mathematical operations. Here are some examples of SimpleScript's mathematical capabilities. All operations are similar to their BASIC implementation. 

---

* [All Supported Operators](#all-supported-operators)
* [Examples Of Math Operations](#examples-of-math-operations)

---

## All Supported Operators

Here is a table including all supported mathematical operations in SimpleScript. Most are similar to Python or BASIC's implementations, but I've made some small changes which hopefully improve the look and feel of larger mathematical expressions.

| Operation | SimpleScript Command | Description | Notes |
|---|---|---|---|
| Addition | + | Performs addition |  |
| Subtraction | - | Performs subtraction |  |
| Multiplication | * | Performs multiplication |  |
| Division | / | Performs typical floating division | Cannot divide by 0 |
| Integer Division | &#124; | Performs division using integers | Cannot divide by 0 |
| Power | ^ | Raises expression to a power | Supports negative powers |
| Modulo | % | Returns remainder of division |  |

All these operations can be performed on both numeric values and sub-expressions, including variables. Variables are executed before any other numeric operation, so you can actually assign variables _while performing numeric operations_ on other values. 

## Examples Of Math Operations

Basic arithmetic operations can be performed directly on numbers, variables, and other values. Mathematical operations all return their associated value. Anytime a floating point operation is introduced, the data type returned will be a float. 

```php
$ (2 + 1) | (4 - 1)
$ 1
```

```php
$ 10 % 5
$ 0
```

```php
$ 1 + 2 - 3 * 4 / 5
$ 0.6000000000000001
```

```php
$ ((1 + 2) * 3 ^ 2) / 2
$ 13.5
```

```php
$ 10 | 2 + (8 ^ 2) - 6
$ 63
```

As you'd expect, division by zero is not allowed. If you try, the interpreter will inform you that the operation you're trying to execute is invalid. It will even highlight the error in your file. Negative powers are valid operations that will evaluate to the same result as would a similar BASIC operation.

```php
$ 12345 / 0

Traceback (most recent call last):
File <stdin>, line 1, in <program>
File <stdin>, on line 1
12345 / 0
        ^
```

```php
$ 98765 / (4 - 5 + 1)

Traceback (most recent call last):
File <stdin>, line 1, in <program>
File <stdin>, on line 1
98765 / (4 - 5 + 1)
         ^^^^^^^^^
```

Operations that eventually evaluate into zero are also not allowed, as seen in the above example. In this case, the entire sub-expression is highlighted by the interpreter. This hopefully provides enough tracing and error information to fix the issue in your program. The stack trace will always be displayed in error messages.