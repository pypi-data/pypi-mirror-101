# This file is placed in the Public Domain.

from botl.bus import Bus
from botl.evt import Command, events
from botl.obj import fmt
from botl.thr import launch
from botl.zzz import random, unittest
from test.prm import param
from test.run import t

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(t.cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()
        t.stop()

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res

def exec():
    l = list(t.modnames)
    random.shuffle(l)
    for cmd in l:
        if cmd not in param:
            e = Command({"txt": cmd, "orig": repr(t)})
            t.put(e)
            events.append(e)
            continue
        for ex in getattr(param, cmd, [""]):
            txt = cmd + " " + ex
            e = Command({"txt": txt, "orig": repr(t)})
            t.put(e)
            events.append(e)
