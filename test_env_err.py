import unittest

from error import *
from environment import *

# error is on the inside, because env operations may fail - unbound symbol.
# is it possible to represent an env error with error on the outside?


class TestEvaluator(unittest.TestCase):

    def test_simple(self):
        k = bind( unit(1), lambda x:
            bind( unit(2), lambda y:
                  unit(x+y)))
        self.assertEquals(2, 3)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestEvaluator))

if __name__=="__main__":
    unittest.main(exit=False)
