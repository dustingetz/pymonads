from monads import *

class _Maybe_m(Monad):
    def bind(self, mv, mf):
        #careful, [] is falsey, which broke m-seq
        return mf(mv) if mv!=None else None
    def unit(self, v): return v

maybe_m = _Maybe_m()


def test():
    dbl = lambda x: 2*x

    assert maybe_m.fmap(dbl, None) == None
    assert maybe_m.fmap(dbl, 2) == 4

    chain = maybe_m.chain
    assert chain(dbl, dbl)(2) == 8
    assert chain(lambda x:None, dbl)(2) == None
    assert chain(dbl, dbl)(2) == 8

    seq = maybe_m.seq
    assert seq([1, 1, 1]) == [1,1,1]
    assert seq([None]) == None
    assert seq([1, None, 1]) == None

    mmap = maybe_m.map
    assert mmap(dbl, [3, 3, 3]) == [6, 6, 6]
    assert mmap(lambda _: None, [3, 3, 3]) == None

    failOdd = lambda x: None if x%2==1 else x
    assert mmap(failOdd, [2, 4, 6]) == [2, 4, 6]
    assert mmap(failOdd, [2, 4, 5, 6]) == None


if __name__=="__main__":
    test()
    print "tests passed: maybe"
