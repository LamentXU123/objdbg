from objdbg import dbg
class A():
    def __init__(self):
        self.s = 1
    def __eq__(self):
        return False

    @staticmethod
    def staticadd(b, v):
        return b + v
    @classmethod
    def classadd(self, c, b=1, v=2):
        return Ellipsis
    def add(self, a, b, c, *args, **kargs):
        return a + b + c
dbg(A())