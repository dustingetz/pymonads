from __future__ import print_function


def identity(x): return x
def _reverse(xs): return xs[-1::-1]

class Monad:
    """provides generic methods like fmap, map, reduce, chain which use polymorphic
    implementations of unit and bind.

    many of the following functions are directly ported from clojure/algo.monads:
    https://github.com/clojure/algo.monads/blob/3d7baa96d9435245f98e395bcddae4427eba1a85/src/main/clojure/clojure/algo/monads.clj#L276
    """

    # these are difficult to use properly without a type checker unless
    # you really know what you're doing.

    def join(self, mv):
        """Converts a monadic value containing a monadic value into a 'simple'
        monadic value."""
        return self.bind(mv, identity)

    def fmap(self, f, mv): # -> mv
        """Bind the monadic value m to the function returning (f x) for
        argument x"""
        return self.bind(mv, lambda x: self.unit(f(x)))

    def seq(self, ms):
        """something is wrong here also, the return types don't make sense.

        'Executes' the monadic values in ms and returns a sequence of the
        basic values contained in them."""
        #print ("ms: %s"%ms)
        def f(q, p):
            #print("p: %s, q: %s"%(p,q))
            return self.bind(p, lambda x:
                   self.bind(q, lambda y:
                   self.unit([x] + y))) #(cons x y)
        return self.join(reduce(f, _reverse(ms), self.unit([])))

    def map(self, mf, xs): # -> [x]
        """map mf over xs 'inside the monad', returning list of simple values?
        something is wrong with this definition, if we're in error-m, if everything
        succeeds we get return type [x], if there is a failure we return mv, that
        doesn't type check.

        'Executes' the sequence of monadic values resulting from mapping
        mf onto the values xs. mf must return a monadic value. return type is [x]"""
        #lazy_ms = (mf(x) for x in xs)
        #return self.seq(lazy_ms)
        return self.seq(map(mf, xs)) # bug, this needs to be lazy ?

    def chain(self, *fns):
        """returns a function of one argument which performs the monadic
        composition of fns."""
        def chain_link(chain_expr, step):
            return lambda v: self.bind(chain_expr(v), step)
        return reduce(chain_link, fns, self.unit)

    # can we define m_lift? it's a macro in clojure

    def reduce(f, mvs):
        """Return the reduction of (m-lift 2 f) over the list of monadic values mvs
        with initial value (m-result val)."""
        pass


    def until():
        """While (p x) is false, replace x by the value returned by the
        monadic computation (f x). Return (m-result x) for the first
        x for which (p x) is true."""
        pass


class _Identity_m(Monad):
    def unit(self, v): return v
    def bind(self, mv, mf): return mf(mv)

identity_m = _Identity_m()

def _test_identity_m():
    dbl = lambda x: 2*x
    assert identity_m.chain(dbl, dbl)(2) == 8
    assert identity_m.map(dbl, [3, 3, 3]) == [6, 6, 6]
    assert identity_m.seq([1, 1, 1]) == [1, 1, 1]

class _Maybe_m(Monad):
    def bind(self, mv, mf):
        #careful, [] is falsey, which broke m-seq
        return mf(mv) if mv!=None else None
    def unit(self, v): return v

maybe_m = _Maybe_m()
def _test_maybe_m():
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





class _Error_m(Monad):
    def bind(self, mv, mf):
        #careful, [] is falsey, which broke m-seq
        #careful, (None, None) does not signal an error, which broke m-seq
        return mf(mv[0]) if mv[1]==None else mv
    def unit(self, v): return (v, None)

error_m = _Error_m()
def ok(val): return (val, None)
def err(msg): return (None, msg)

def _test_error_m():
    chain = error_m.chain
    seq = error_m.seq
    mmap = error_m.map

    assert chain(lambda x:ok(2*x), lambda x:ok(2*x))(2) == (8, None)
    assert chain(lambda x:err("error"), lambda x:ok(2*x))(2) == (None, "error")
    assert chain(lambda x:ok(2*x), lambda x:err("error"))(2) == (None, "error")

    assert seq(map(ok, [1, 1, 1])) == [1,1,1]
    assert seq(map(ok, [1, 1, None, 1])) == [1,1,None,1] #ok(None) is not an error
    assert seq([ok(None), err("error"), ok(1)]) == err("error")

    dbl = lambda x: ok(2*x)
    assert mmap(dbl, [3, 3, 3]) == [6, 6, 6]
    assert mmap(lambda _: err("error"), [3, 3, 3]) == err("error")

    failOdd = lambda x: err("odd") if x%2==1 else ok(x)
    assert mmap(failOdd, [2, 4, 6]) == [2, 4, 6]
    assert mmap(failOdd, [2, 4, 5, 6]) == err("odd")




from itertools import chain
def _flatten(listOfLists):
    "Flatten one level of nesting"
    return list(chain.from_iterable(listOfLists))

class _List_m(Monad):
    def unit(self, v): return [v]
    def bind(self, mv, mf): return _flatten(map(mf, mv))

list_m = _List_m()

def _test_list_m():
    assert list_m.bind(range(5), lambda x: list_m.unit(x*2)) == [0,2,4,6,8]

    # equivalent to [y for x in range(5) for y in range(x)]
    assert list_m.chain(range, range)(5) == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3]
    assert list_m.bind(range(5), range) == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3]

    def _chessboard():
        ranks = list("abcdefgh")
        files = list("12345678")

        return list_m.bind(ranks, lambda rank:
               list_m.bind(files, lambda file:
               list_m.unit((rank, file))))

    assert len(_chessboard()) == 64
    assert _chessboard()[:3] == [('a', '1'), ('a', '2'), ('a', '3')]

    # concept of map generalizes to monad operatons that aren't list
    # comprehensions:
    assert list_m.fmap(lambda x:2*x, range(5)) == [0,2,4,6,8]



class _Writer_m(Monad):

    def unit(self, v): return (v, [])
    def get_val(self, mv): return mv[0]
    def get_out(self, mv): return mv[1]

    def bind(self, mv, mf):
        val, out = self.get_val(mv), self.get_out(mv)
        r_mv = mf(val)
        r_out = self.get_out(r_mv)
        final_out = out + r_out if r_out else out
        return (self.get_val(r_mv), final_out)

writer_m = _Writer_m()

def _test_writer_m():
    def withlog(val, out): return (val, [out])
    def nolog(val): return (val, [])

    def addOne(x):
        x=x+1
        return withlog(x, "x+1==%s"%x)

    assert writer_m.chain(addOne, addOne, addOne)(7) == (10, ['x+1==8', 'x+1==9', 'x+1==10'])

    r = writer_m.bind( withlog(7, "init as 7"), lambda x:
        writer_m.bind( withlog(x+1, "+1"), lambda y:
        writer_m.bind( nolog(y), lambda z:
        writer_m.bind( withlog(x+y+z, "sum the steps"), lambda a:
        writer_m.unit( a )))))

    assert r == (23, ['init as 7', '+1', 'sum the steps'])


class _Reader_m(Monad):
    def unit(self, v): return lambda env: v
    def bind(self, mv, mf):
        def _(env):
            val = mv(env)
            return mf(val)(env)
        return _

reader_m = _Reader_m()
def ask(env): return env

def _test_reader_m():
    bind = reader_m.bind
    unit = reader_m.unit
    fmap = reader_m.fmap

    def getA(env): return env["a"]

    def f1(): return fmap(ask, lambda env: env["a"])
    def f2(): return fmap(getA, lambda a: a)

    env = {"a": "42"}
    assert f1()(env) == "42"
    assert f2()(env) == "42"



def _run_tests():
    _test_identity_m()
    _test_maybe_m()
    _test_error_m()
    _test_list_m()
    _test_writer_m()
    _test_reader_m()
    print("all tests passed")


if __name__=="__main__": _run_tests()
