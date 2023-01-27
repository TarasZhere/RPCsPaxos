from threading import Thread

class ThreadReturn(Thread):
    
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.__return = None


    def run(self):
        if self._target is not None:
            self.__return = self._target(*self._args, **self._kwargs)


    def join(self, *args):
        Thread.join(self, *args)
        return self.__return