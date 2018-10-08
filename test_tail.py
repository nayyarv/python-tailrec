#!/usr/bin/env py.test

"""
We test that the `Tailrec` wrapper actually returns expected results and that
it does optimize the tail recursion as expected by checking that it doesn't
raise a recursion error when compared to the naive methods.

We also check that the ASTTailrec provides identical behaviour

The recursion depth in the test is set at `10 * sys.getrecursionlimit()`
`sys.getrecursionlimit()` defaults to 1000.
"""
import sys
import pytest
from tailrec import Tailrec, ASTTailrec


@Tailrec
def fac(n, k=1):
    if n == 0:
        return k
    else:
        return fac.recur(n=n - 1, k=n * k)


@ASTTailrec
def fac_ast(n, k=1):
    if n == 0:
        return k
    else:
        return fac(n=n - 1, k=n * k)


def test_example_base():
    from operator import mul
    from functools import reduce
    assert fac(200) == reduce(mul, (range(1, 201)))

def test_example_ast():
    from operator import mul
    from functools import reduce
    assert fac_ast(200) == reduce(mul, (range(1, 201)))


RECURSE_TEST = sys.getrecursionlimit() * 10


def add_recur(a, b):
    if a == 0: return b
    return add_recur(a - 1, b + 1)


def test_recurse_error():
    with pytest.raises(RecursionError):
        add_recur(RECURSE_TEST, 0)


@Tailrec
def add_recur_tail(a, b):
    if a == 0: return b
    return add_recur_tail.recur(a - 1, b + 1)


def test_no_recurse_error_base():
    add_recur_tail(RECURSE_TEST, 0) == RECURSE_TEST


@ASTTailrec
def add_recur_ast(a, b):
    if a <= 0: return b
    return add_recur_ast(a - 1, b + 1)


def test_no_recurse_error_ast():
    add_recur_ast(RECURSE_TEST, 0) == RECURSE_TEST
