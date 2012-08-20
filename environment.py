from monads import *


class _Environment_m(Monad):
    "writer inside reader, for maps. identitcal to state monad."

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
    def ask_m(env): return (v, env)

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



class Environment_t(_Environment_m):
    def __init__(self, basemonad):
        self.base_m = basemonad

    def unit(self, v):
        bunit = self.base_m.unit

        return lambda env: bunit((v, env))

    def bind(self, mv, mf):
        bbind = self.base_m.bind

        def _env_mv(env):
            return bbind( mv(env), lambda st_val: # st_val is (val, newenv)
                          mf(st_val[0])(st_val[1]))
        return _env_mv



env_m = _Environment_m() #equivalently, Environment_t(identity_m)

def _testm(env_m):
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

    print runIn(r, {})
    assert runIn(r, {}) == 5
    assert runIn(r, {"a":0}) == 5
    assert seq([r,r,r])({}) == ([5, 5, 5], {'a': 2, 'c': 5, 'b': 3})

    assert mmap(unit, [1,2,3])({}) == ([1, 2, 3], {})
    assert fmap(identity, r)({})[0] == 5

    r = bind(get("c"), lambda c: unit(c))
    assert runIn(r, {"c":42}) == 42
    assert runIn(r, {"c":43}) == 43

def test():
    #test both the monad and the monad transformers
    from identity import identity_m

    _testm(env_m)
    _testm(Environment_t(identity_m))

if __name__=="__main__":
    test()
    print "tests passed: environment"
