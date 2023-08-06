# This file is placed in the Public Domain.

"threads"

import queue
import threading
import time
import types

from .obj import Default, getname
from .trc import exception

starttime = time.time()

class Thr(threading.Thread):

    def __init__(self, func, *args, thrname="", daemon=True):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._name = thrname or get_name(func)
        self._result = None
        self._queue = queue.Queue()
        self._queue.put_nowait((func, args))
        self.sleep = 0

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        ""
        super().join(timeout)
        return self._result

    def run(self):
        ""
        func, args = self._queue.get_nowait()
        if args:
            try:
                target = Default(vars(args[0]))
                self._name = (target and target.txt and target.txt.split()[0]) or self._name
            except (IndexError, TypeError):
                pass
        self.setName(self._name)
        try:
            self._result = func(*args)
        except Exception as ex:
            print(exception())

def launch(func, *args, **kwargs):
    name = kwargs.get("name", getname(func))
    t = Thr(func, *args, thrname=name, daemon=True)
    t.start()
    return t
