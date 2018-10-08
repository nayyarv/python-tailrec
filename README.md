# ASTTailrec

**What it is:**
`tailrec` is a toy Python module for writing tail-recursive functions without exceeding the recursion limit. 

It does two things:

1. Wraps the function to allow for the recursive calls to be evaluated iteratively thus avoiding the recursion depth limit. Note this means most recursive solutions will still be quite slow.
2. It uses AST manipulation to allow for the function to be written using tail recursion and with no special tricks. You can write natural tail recursion code and stick the decorator on top.

**Example:**

```python
from tailrec import ASTTailrec

@ASTTailrec
def fac(n, k = 1):
    if n == 1:
        return k
    return fac(n = n - 1, k = n * k)

print("200! =", fac(200))
```

**Caveats**

1. No error checking or even tail recursion checking - if you add this to a non-tail recursive function, this will not sidestep the recursion
2. Limited error checking and debugging - the AST manipulation means errors and code printed may not match.
3. `inspect.getsource` does not work for an unidentified reason at this time.

**Credits**

1. https://github.com/ac1235/python-tailrec - for the first implementation of tail recursion, in fact this project is forked from the above. All this project does is to add the AST approach to allow even more natural code writing.
2. https://github.com/robinhilliard/pipes - for presenting this library at a Python meetup and explaining how the AST manipulation works. I have used his skeletons in setup and teardown instead of writing my own. 