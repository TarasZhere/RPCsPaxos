import inspect
class Da:
    def __init__(self) -> None:
        self.m = 2
        pass

    def test(self, e):
        self.m += e
        print(e)

    def test2(self, e):
        print('M:', self.m)
        print(e)


ls = inspect.getmembers(Da)

for name, func in ls:
    if name[0] != '_':
        print(name)
        print(func())