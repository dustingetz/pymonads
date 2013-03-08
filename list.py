from monads import *


from itertools import chain
def _flatten(listOfLists):
    "Flatten one level of nesting"
    return list(chain.from_iterable(listOfLists))

class _List_m(Monad):
    def unit(self, v): return [v]
    def bind(self, mv, mf): return _flatten(map(mf, mv))

list_m = _List_m()

def test():
    bind, unit = list_m.bind, list_m.unit

    assert bind(range(5), lambda x: unit(x*2)) == [0,2,4,6,8]

    # equivalent to [y for x in range(5) for y in range(x)]
    assert list_m.chain(range, range)(5) == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3]
    assert bind(range(5), range) == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3]

    def _chessboard():
        ranks = list("abcdefgh")
        files = list("12345678")

        return bind(ranks, lambda rank:
               bind(files, lambda file:
               unit((rank, file))))

    assert len(_chessboard()) == 64
    assert _chessboard()[:3] == [('a', '1'), ('a', '2'), ('a', '3')]

    # concept of map generalizes to monad operatons that aren't list
    # comprehensions:
    assert list_m.fmap(lambda x:2*x, range(5)) == [0,2,4,6,8]


if __name__=="__main__":
    test()
    print "tests passed: list"
