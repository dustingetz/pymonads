from monads import *


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

def test():
    def withlog(val, out): return (val, [out])
    def nolog(val): return (val, [])

    def addOne(x):
        x=x+1
        return withlog(x, "x+1==%s"%x)


    chain = writer_m.chain
    assert chain(addOne, addOne, addOne)(7) == (10, ['x+1==8', 'x+1==9', 'x+1==10'])

    bind, unit = writer_m.bind, writer_m.unit

    r = writer_m.bind( withlog(7, "init as 7"), lambda x:
        writer_m.bind( withlog(x+1, "+1"), lambda y:
        writer_m.bind( nolog(y), lambda z:
        writer_m.bind( withlog(x+y+z, "sum the steps"), lambda a:
        writer_m.unit( a )))))
    assert r == (23, ['init as 7', '+1', 'sum the steps'])

    mmap = writer_m.map
    assert mmap(addOne, [1,2,3]) == ([2, 3, 4], ['x+1==2', 'x+1==3', 'x+1==4'])

    addThreeLogged = chain(addOne, addOne, addOne)
    assert map(addThreeLogged, [10,20,30]) == [
        (13, ['x+1==11', 'x+1==12', 'x+1==13']),
        (23, ['x+1==21', 'x+1==22', 'x+1==23']),
        (33, ['x+1==31', 'x+1==32', 'x+1==33'])]


if __name__=="__main__":
    test()
    print "tests passed: writer"
