"""
Tail recursion should be as simple as a decorator

This uses the AST of python to do the rewriting to reduce to existing Tailrec implementation
"""
import ast

from inspect import getsource, isclass
from textwrap import dedent

from tailrec import Tailrec, Tailcall

__all__ = ["ASTTailrec"]


class TailTransformer(ast.NodeTransformer):
    """
    Replace all the return statements we see that are just recursive function calls
    to the same name with `name.recur`
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super(TailTransformer).__init__(*args, **kwargs)

    def visit_Return(self, node):
        if isinstance(node.value, ast.Call):
            if node.value.func.id == self.name:
                # Since the dot syntax means that this an attribute call and not a function call, 
                # we have to create a new node.
                node.value.func = ast.Attribute(value=node.value.func, attr="recur", ctx=ast.Load())
        # creating a new node doesn't always play nice with compile,
        # so fix missing locations automatically
        ast.fix_missing_locations(node)
        return node


def replace_decorator(func_tree):
    """
    The ASTTailrec decorator wants to get rid of itself and replace with Tailrec so we can
    reduce this problem to already solved issue.

    """
    decorators = func_tree.body[0].decorator_list
    for dec in decorators:
        if dec.id == 'ASTTailrec':
            dec.id = 'Tailrec'


def ASTTailrec(func):
    """
    This approach involves modifying the ast tree so we can just stick a decorator on such as

    ```
    @ASTTailrec
    def fac(n, k=1):
        if n == 1: return k
        return fac(n-1, k*n)
    ```

    This function has been heavily inspired by  Robin Hillard's pipeop library at
    https://github.com/robinhilliard/pipes. It was used as reference when developing this decorator
    """
    if isclass(func):
        raise TypeError("Cannot apply tail recursion to a class")

    in_context = func.__globals__

    new_context = {"Tailrec": Tailrec, "Tailcall": Tailcall}

    # these need to be included in the imports else we're gonna have some trouble
    # if they've already been imported, let that import hold precedence.
    new_context.update(in_context)

    # now let's try and get the source
    source = getsource(func)
    # we get the tree
    tree = ast.parse(dedent(source))

    # update for debugger
    first_line_number = func.__code__.co_firstlineno
    ast.increment_lineno(tree, first_line_number - 1)

    # let's grab the name of the function here. func.__name__ is not reliable in case
    # of other decorators and no use of `functools.wraps`
    func_name = tree.body[0].name

    # we want to replace with the standard tailrec decorator here
    replace_decorator(tree)

    # now every time we find the function, let's replace with func_name.recur
    # as in the standard case
    tree = TailTransformer(func_name).visit(tree)

    # now the tree has been modified satisfactorily, let's compile
    code = compile(tree, filename=new_context['__file__'], mode='exec')

    # exec the code in the scope of the new_context
    exec(code, new_context)

    # and return the function
    return new_context[func_name]
