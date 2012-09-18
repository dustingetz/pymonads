from monads import *

class _Cont_m(Monad):
    """Monad describing computations in continuation-passing style. The monadic
    values are functions that are called with a single argument representing
    the continuation of the computation, to which they pass their result."""

    def unit(self, v):
        return lambda c: c(v)

    def bind(self, mv, mf):
        def _cont_mv(c):
            return mv(lambda v: mf(v)(c))
        return _cont_mv

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

class Cont_t(_Cont_m):
    """"http://www.haskell.org/ghc/docs/6.10.4/html/libraries/mtl/src/Control-Monad-Cont.html#ContT"""

    def __init__(self, basemonad):
        self.base_m = basemonad

    def unit(self, v):
        bunit = self.base_m.unit

        return lambda c: c(bunit(v))

    def bind(self, mv, mf):
        bbind = self.base_m.bind

        def _cont_mv(c):
            # return bbind( mv, lambda cont_val:
            #               mf(cont_val)(c))
            return bbind( mv, lambda cont_val:
                          cont_val(lambda v: mf(v)(c)))
        return _cont_mv

from identity import identity_m
cont_m = Cont_t(identity_m) #_Cont_m()


if __name__=="__main__":
    import unittest
    import test_continuation
    unittest.TextTestRunner().run(test_continuation.suite)
