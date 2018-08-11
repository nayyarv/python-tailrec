# tailrec

**What it is:**
`tailrec` is a Python module for writing tail-recursive functions without exceeding the recursion limit.

**How it works:**
A function decorated with `@Tailrec` can tail call itself or any other `Tailrec` object using `func.recur(...)` in a tail-position (that is directly before a `return`). Calling `recur` on a regular function object fails. In order to prevent this `Tailrec(func).recur(...)` can be used instead of just `func.recur(...)` in places where `func` may not be a `Tailrec`.

**Example:**

```python
from tailrec import Tailrec

@Tailrec
def fac(n, k = 1):
    if n == 0:
        return k
    else:
        return fac.recur(n = n - 1, k = n * k)

print("200! =", fac(200))
```
