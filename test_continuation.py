import unittest

from continuation import *


bind, unit = cont_m.bind, cont_m.unit
runCont, callcc = cont_m.runCont, cont_m.callcc

class TestEvaluator(unittest.TestCase):

    def test_simple(self):
        """A simple computation performed in continuation-passing style.
        (m-result 1) returns a function that, when called with a single
        argument f, calls (f 1). The result of the domonad-computation is
        a function that behaves in the same way, passing 3 to its function
        argument. run-cont executes a continuation by calling it on identity."""
        k = bind( unit(1), lambda x:
            bind( unit(2), lambda y:
                  unit(x+y)))

        self.assertEquals(runCont(k), 3)

    def test_callcc(self):
        """Let's capture a continuation using call-cc. We store it in a global
        variable so that we can do with it whatever we want. The computation
        is the same one as in the first example, but it has the side effect
        of storing the continuation at (m-result 2)."""

        global cont
        cont = 77

        def f(c):
            global cont
            cont = c
            return c(2)

        k = bind( unit(1), lambda x:
            bind( callcc(f), lambda y:
                  unit(x+y)))
        self.assertEqual(runCont(k), 3)

        # Now we can call the continuation with whatever argument we want. The
        # supplied argument takes the place of 2 in the above computation:
        self.assertEqual(runCont(cont(5)), 6)
        self.assertEqual(runCont(cont(42)), 43)
        self.assertEqual(runCont(cont(-1)), 0)




suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestEvaluator))

if __name__=="__main__":
    unittest.main(exit=False)
