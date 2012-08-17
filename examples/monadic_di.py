from collections import namedtuple
from monads import reader_m



class Servlet:
    def __init__(log, settings):
        self.log = log
        self.settings = settings

    def post(request, db): pass
    def get(request, db): pass

class PageServlet(Servlet): pass
class DatastoreServlet(Servlet): pass



Env = namedtuple('Env', ['hostname', 'port', 'outfile'])
# getters describe how to read a value from an environment,
# but do not have access to the environment itself
hostname = lambda env: env.hostname
port = lambda env: env.port
outfile = lambda env: env.outfile

servlets = []

def doSomething(h,p,o): return [o, p, h]

def bootstrap():
    """no dependencies passed as parameters. could have very long list of
    dependencies"""
    r = reader_m.bind( hostname, lambda h:
        reader_m.bind( port,     lambda p:
        reader_m.bind( outfile,  lambda o:
        reader_m.unit( doSomething(h,p,o) ))))
    return r

env = Env("localhost", 80, "/etc/passwd")
assert bootstrap()(env) == ["/etc/passwd", 80, "localhost"]
