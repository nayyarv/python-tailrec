#!/usr/bin/py.test

from asttailrec import ASTTailRec
import pytest

@ASTTailRec
def add_recur(a, b):
    if a <= 0: return b
    return add_recur(a-1, b+1)

def add(a, b):
    if a <= 0: return b
    return add(a-1, b+1)


def test_recurse_error():
    with pytest.raises(RecursionError):
        add(1e5, 0)

def test_no_recurse_error():
    add_recur(1e5, 0)


if __name__ == '__main__':
    add_recur(10, 0)
