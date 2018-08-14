#!/usr/bin/env py.test

import pytest
from tailrec import Tailrec


def add_recur(a, b):
    if a == 0: return b
    return add_recur(a - 1, b + 1)


@Tailrec
def add_tail(a, b):
    if a == 0: return b
    return add_tail.recur(a - 1, b + 1)


@Tailrec
def fac(n, k=1):
    if n == 0:
        return k
    else:
        return fac.recur(n=n - 1, k=n * k)


def test_example():
    from operator import mul
    from functools import reduce
    assert fac(200) == reduce(mul, (range(1, 201)))


def test_recurse_error():
    with pytest.raises(RecursionError):
        add_recur(1e5, 0)


def test_no_recurse_error():
    add_tail(1e5, 0)


def test_funny():
    from inspect import getsource
    print(fac.__name__)
    getsource(fac)
