from monads import *


class _Error_m(Monad):
    def bind(self, mv, mf):
        #careful, [] is falsey, which broke m-seq
        #careful, (None, None) does not signal an error, which broke m-seq
        return mf(mv[0]) if mv[1]==None else mv
    def unit(self, v): return self.ok(v)

    @staticmethod
    def ok(val): return (val, None)

    @staticmethod
    def err(msg): return (None, msg)


error_m = _Error_m()

def test():
    chain = error_m.chain
    seq = error_m.seq
    mmap = error_m.map
    join = error_m.join
    bind, unit = error_m.bind, error_m.unit
    ok, err = error_m.ok, error_m.err

    assert chain(lambda x:ok(2*x), lambda x:ok(2*x))(2) == (8, None)
    assert chain(lambda x:err("error"), lambda x:ok(2*x))(2) == (None, "error")
    assert chain(lambda x:ok(2*x), lambda x:err("error"))(2) == (None, "error")

    assert seq(map(ok, [1, 1, 1])) == ok([1,1,1])
    assert seq(map(ok, [1, 1, None, 1])) == ok([1,1,None,1]) #ok(None) is not an error
    assert seq([ok(None), err("error"), ok(1)]) == err("error")

    dbl = lambda x: ok(2*x)
    assert mmap(dbl, [3, 3, 3]) == ok([6, 6, 6])
    assert mmap(lambda _: err("error"), [3, 3, 3]) == err("error")

    failOdd = lambda x: err("odd") if x%2==1 else ok(x)
    assert mmap(failOdd, [2, 4, 6]) == ok([2, 4, 6])
    assert join(mmap(failOdd, [2, 4, 6])) == [2, 4, 6]
    assert mmap(failOdd, [2, 4, 5, 6]) == err("odd")

    #print bind(mmap(failOdd, [2, 4, 5, 6]), lambda x: unit(x))
    #print bind(mmap(failOdd, [2, 4, 5, 6]), lambda x: x)




if __name__=="__main__":
    test()
    print "tests passed: error"
