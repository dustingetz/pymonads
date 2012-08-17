from monads import *


class _Reader_m(Monad):
    def unit(self, v): return lambda env: v
    def bind(self, mv, mf):
        def _(env):
            val = mv(env)
            return mf(val)(env)
        return _

reader_m = _Reader_m()
def ask(env): return env

def test():
    bind = reader_m.bind
    unit = reader_m.unit
    fmap = reader_m.fmap

    def getA(env): return env["a"]

    def f1(): return fmap(ask, lambda env: env["a"])
    def f2(): return fmap(getA, lambda a: a)

    env = {"a": "42"}
    assert f1()(env) == "42"
    assert f2()(env) == "42"


if __name__=="__main__":
    test()
    print "tests passed: reader"
