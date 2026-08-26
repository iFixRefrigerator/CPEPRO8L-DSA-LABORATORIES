# Lab 05: Stack Parenthesis Arithmetic Parser

## Objectives

1. Build a custom Stack class using a dynamic list (Python list).
2. Design an algorithm to check for balanced bracket pairs `()`, `[]`, `{}`.
3. Understand stack push/pop tracking in expression parsers.

## Execution & Output

### Console Output
```
Is '{{()}}' balanced? True
Is '{{()}' balanced? False
Is '{[()]}' balanced? True
Is '([)]' balanced? False
Is '((()))' balanced? True
```


### Algorithm Trace for "{{()}}"

**Step-by-step stack visualization:**

| Step | Character | Operation | Stack State (bottom → top) |
|------|-----------|-----------|----------------------------|
| 0    | -         | Initial   | []                         |
| 1    | `{`       | Push      | `[ { ]`                    |
| 2    | `{`       | Push      | `[ {, { ]`                 |
| 3    | `(`       | Push      | `[ {, {, ( ]`              |
| 4    | `)`       | Pop       | `[ {, { ]`                 |
| 5    | `}`       | Pop       | `[ { ]`                    |
| 6    | `}`       | Pop       | `[]`                       |

**Final check:** Stack is empty → Expression is **balanced** ✅

### Algorithm Trace for "{{()}" (unbalanced)

| Step | Character | Operation | Stack State (bottom → top) |
|------|-----------|-----------|----------------------------|
| 0    | -         | Initial   | []                         |
| 1    | `{`       | Push      | `[ { ]`                    |
| 2    | `{`       | Push      | `[ {, { ]`                 |
| 3    | `(`       | Push      | `[ {, {, ( ]`              |
| 4    | `)`       | Pop       | `[ {, { ]`                 |
| 5    | `}`       | Pop       | `[ { ]`                    |

**Final check:** Stack is NOT empty → Expression is **unbalanced** ❌

---

## Report Analysis Questions

### 1. Implement the solution and verify it against 5 customized mathematical expressions

**Test Expressions and Results:**

| # | Expression | Expected | Actual | Reason |
|---|------------|----------|--------|--------|
| 1 | `{[()]}`   | True     | True   | Properly nested brackets |
| 2 | `([)]`     | False    | False  | Mismatched closing brackets |
| 3 | `((()))`   | True     | True   | Perfectly nested parentheses |
| 4 | `{[(])}`   | False    | False  | Wrong order of closing brackets |
| 5 | `[]{}()`   | True     | True   | Multiple independent pairs |

### 2. Draw the state of the stack at each loop step when evaluating "{{()}}"

**Detailed Step-by-Step Trace:**

**Expression: `{{()}}`**

| Iteration | Character | Action | Stack Contents (Bottom → Top) | Output |
|-----------|-----------|--------|------------------------------|--------|
| Start | - | Initialize | `[]` | - |
| 1 | `{` | Push `{` | `[{]` | Continue |
| 2 | `{` | Push `{` | `[{, {]` | Continue |
| 3 | `(` | Push `(` | `[{, {, (]` | Continue |
| 4 | `)` | Pop `(` | `[{, {]` | Match found |
| 5 | `}` | Pop `{` | `[{]` | Match found |
| 6 | `}` | Pop `{` | `[]` | Match found |

**Final: Stack is empty → Return True**

---

## How to Run

```bash
python lab05_bracket_parser.py

## Files

- `lab05_bracket_parser.py` - Main Python script with Stack implementation and balanced bracket checker
- `README.md` - This documentation file

## Author

**YOUR NAME HERE**

## GitHub Repository

[https://github.com/FuRefrigerator/CPEPROBL-DSA-LABORATORIES](https://github.com/FuRefrigerator/CPEPROBL-DSA-LABORATORIES)
