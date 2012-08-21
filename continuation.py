from monads import *

class _Cont_m(Monad):
    """Monad describing computations in continuation-passing style. The monadic
    values are functions that are called with a single argument representing
    the continuation of the computation, to which they pass their result."""

    def unit(self, v):
        return lambda c: c(v)

    def bind(self, mv, mf):
        return lambda c: mv(lambda v: mf(v)(c))

    @staticmethod
    def runCont(c):
        "Execute the computation c in the cont monad and return its result."
        return c(identity)

    @staticmethod
    def callcc(f):
        """A computation in the cont monad that calls function f with a single
        argument representing the current continuation. The function f should
        return a continuation (which becomes the return value of call-cc),
        or call the passed-in current continuation to terminate."""
        def _(c):
            cc = lambda a: lambda _: c(a)
            rc = f(cc)
            return rc(c)
        return _


cont_m = _Cont_m()


if __name__=="__main__":
    import unittest
    import test_continuation
    unittest.TextTestRunner().run(test_continuation.suite)
