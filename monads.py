
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



def _run_tests():
    import identity, maybe, error, list, writer, reader
    identity.test()
    maybe.test()
    error.test()
    list.test()
    writer.test()
    reader.test()
    print("all tests passed")


if __name__=="__main__": _run_tests()
