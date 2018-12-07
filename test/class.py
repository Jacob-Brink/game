class A:
    def __init__(self):
        print('A was initialized')
    def a_func(self):
        print('a func worked')

class B:
    def __init__(self):
        print('B was initialized')
    def b_func(self):
        print('b func worked')

class Test(B, A):
    def __init__(self):
        super(Test, self).__init__()
        print('initializing Test')
        self.a_func()
t = Test()
