from monads import *


class _Environment_m(Monad):
    "writer inside reader, for maps"

    def unit(self, v):
        return lambda env: (v, env)

    def bind(self, mv, mf):
        def _env_mv(env):
            val, newenv = mv(env)
            return mf(val)(newenv)
        return _env_mv


    @staticmethod
    def runIn_s(mv, env): return mv(env)[0]

    @staticmethod
    def ask_m(env): return env_m.unit(env) #how evil is this global, haha

    @staticmethod
    def set_m(pair):
        def _(env):
            newenv = env.copy()
            newenv.update([pair])
            return None, newenv
        return _

    @staticmethod
    def get_m(sym):
        def _(env):
            return env[sym], env
        return _

env_m = _Environment_m()

def test():
    bind = env_m.bind
    unit = env_m.unit
    fmap, mmap = env_m.fmap, env_m.map
    get = env_m.get_m
    set = env_m.set_m
    runIn = env_m.runIn_s
    seq = env_m.seq
    join = env_m.join

    r = bind(  set(("a", 2)),    lambda _:
        bind(  set(("b", 3)),    lambda _:
        bind(  get("a"),         lambda a:
        bind(  get("b"),         lambda b:
        bind(  set(("c", a+b)),  lambda _:
        bind(  get("c"),         lambda c:
               unit(c)           ))))))

    assert runIn(r, {}) == 5
    assert runIn(r, {"a":0}) == 5
    assert seq([r,r,r])({}) == ([5, 5, 5], {'a': 2, 'c': 5, 'b': 3})

    assert mmap(unit, [1,2,3])({}) == ([1, 2, 3], {})
    assert fmap(identity, r)({})[0] == 5

    r = bind(get("c"), lambda c: unit(c))
    assert runIn(r, {"c":42}) == 42
    assert runIn(r, {"c":43}) == 43



if __name__=="__main__":
    test()
    print "tests passed: environment"
