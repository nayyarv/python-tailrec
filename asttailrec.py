"""
Tail recursion should be as simple as a decorator
A basic implementation here
"""
import ast


from inspect import getsource, isclass
from textwrap import dedent
from itertools import takewhile

from tailrec import Tailrec, Tailcall

__all__ = ["ASTTailRec"]

class TailTransformer(ast.NodeTransformer):
    """
    Replace all the return statements we see that are just function calls
    to the same function
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        super(TailTransformer).__init__(*args, **kwargs)

    def visit_Return(self, node):
        print(ast.dump(node))
        if isinstance(node.value, ast.Call):
            if node.value.func.id == self.name:
                ctx = node.value.func.ctx
                # node.value.func.attr = "recur"
                node.value.func = ast.Attribute(value=node.value.func, attr="recur", ctx=ast.Load())
        ast.fix_missing_locations(node)
        print(ast.dump(node))
        return node


def replace_decorator(func_tree):
    """
    The ASTTailRec decorator wants to get rid of itself and replace
    with Tailrec. 
    """
    decorators = func_tree.body[0].decorator_list
    for dec in decorators:
        if dec.id == 'ASTTailRec':
            dec.id = 'Tailrec'


def ASTTailRec(func):
    """
    This approach involves modifying the ast tree and is heavily inspired by 
    Robin Hillard's pipeop library at https://github.com/robinhilliard/pipes
    which was used as a reference when developing this decorator
    """
    if isclass(func):
        raise TypeError("Cannot apply tail recursion to a class")

    in_context = func.__globals__

    new_context = {"Tailrec": Tailrec, "Tailcall": Tailcall}
    # these need to be included in the imports else we're gonna have some trouble
    # if they've already been imported, let that import hold precendece.
    new_context.update(in_context)


    # now let's try and get the source
    source = getsource(func)
    # we get the tree
    tree = ast.parse(dedent(source))
    # print(ast.dump(tree))


    # update for debugger
    first_line_number = func.__code__.co_firstlineno
    ast.increment_lineno(tree, first_line_number - 1)
    source_indent = sum([1 for _ in takewhile(str.isspace, source)]) + 1

    
    # let's grab the name of the function here
    func_name = tree.body[0].name

    # we want to replace with the standard tailrec decorator here
    replace_decorator(tree)

    # now everytime we find the function, let's replace with func_name.recur
    # as in the standard case
    tree = TailTransformer(func_name).visit(tree)
    # print(ast.dump(tree))

    # now the tree has been modified satisfactorily, let's compile
    code = compile(tree, filename=new_context['__file__'], mode='exec')

    # exec
    exec(code, new_context)

    # and return the function
    # print(ast.dump(tree))
    return new_context[func_name]

