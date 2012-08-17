from monads import *


class _Environment_m(Monad):
    "writer inside reader, for maps"

    def unit(self, v):
        return lambda env: (v, {})

    def bind(self, mv, mf):
        def _(env):
            val, newenv = mv(env)
            return mf(val)(newenv)
        return _

env_m = _Environment_m()

def ask(env): return env, env

def set(pair):
    def _(env):
        newenv = env.copy()
        newenv.update([pair])
        return None, newenv
    return _

def get(sym):
    def _(env):
        return env[sym], env
    return _




def test():
    bind = env_m.bind
    unit = env_m.unit
    fmap = env_m.fmap

    r = bind(  set(("a", 2)),    lambda _:
        bind(  set(("b", 3)),    lambda _:
        bind(  get("a"),         lambda a:
        bind(  get("b"),         lambda b:
        bind(  set(("c", a+b)),  lambda _:
        bind(  get("c"),         lambda c:
               unit(c)           ))))))

    assert r({}) == unit(5)({})

    r = bind(get("c"), lambda c: unit(c))
    assert r({"c":42}) == unit(42)({})
    assert r({"c":43}) == unit(43)({})



if __name__=="__main__":
    test()
    print "tests passed: environment"
