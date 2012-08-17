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

    assert writer_m.chain(addOne, addOne, addOne)(7) == (10, ['x+1==8', 'x+1==9', 'x+1==10'])

    r = writer_m.bind( withlog(7, "init as 7"), lambda x:
        writer_m.bind( withlog(x+1, "+1"), lambda y:
        writer_m.bind( nolog(y), lambda z:
        writer_m.bind( withlog(x+y+z, "sum the steps"), lambda a:
        writer_m.unit( a )))))

    assert r == (23, ['init as 7', '+1', 'sum the steps'])


if __name__=="__main__":
    test()
    print "tests passed: writer"
