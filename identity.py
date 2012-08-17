from monads import *

class _Identity_m(Monad):
    def unit(self, v): return v
    def bind(self, mv, mf): return mf(mv)

identity_m = _Identity_m()

def test():
    dbl = lambda x: 2*x
    assert identity_m.chain(dbl, dbl)(2) == 8
    assert identity_m.map(dbl, [3, 3, 3]) == [6, 6, 6]
    assert identity_m.seq([1, 1, 1]) == [1, 1, 1]

if __name__=="__main__":
    test()
    print "test passed: identity"
