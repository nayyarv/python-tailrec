class Tailrec:
    def __init__(self, oper):
        if isinstance(oper, Tailrec):
            self.func = oper.func
        else:
            self.func = oper

    def __call__(self, *args, **kwargs):
        tailpos = self.func(*args, **kwargs)
        while isinstance(tailpos, Tailcall):
            tailpos = tailpos.evaluate()
        return tailpos

    def recur(self, *args, **kwargs):
        return Tailcall(self.func, args, kwargs)

class Tailcall:
    def __init__(self, oper, args, kwargs):
        if isinstance(oper, Tailrec):
            self.func = oper.func
        else:
            self.func = oper
        self.args = args
        self.kwargs = kwargs

    def evaluate(self):
        return self.func(*self.args, **self.kwargs)


