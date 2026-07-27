from __future__ import annotations
from typing import Any, Callable, Iterator
from dataclasses import dataclass as dtc, field;  from random import random as r
from .BaseModels import ManipulatorSet as ms, SizedType as st, TypedType as tt, MemorySizedType as mst

@dtc(slots=True)
class RadioActiveM:   
    def iterate(self, obj, base_action: Callable[[], Any]) ->Iterator[Any]:
        if obj._values==set(): return base_action()
        d=obj._values.copy(); s={(i, r() ):e for i, e in enumerate(obj._values)}
        if r() >= (m:=max(s, key=lambda x: x[1]) )[1] >= r(): obj.discard(s[m])
        return iter(d)
        


class RadioActiveSet(ms):
    """RadioActiveSet enforces random decay. on each iteration there's a chance for an element to get removed(sometimes nothing happens too)"""
    
    def __init__(self, *args, **kwargs): super().__init__(RadioActiveM(), *args, **kwargs)


class SizedSet(st, ms): pass
    

class TypedSet(tt, ms): pass
    
    
class MemorySizedSet(mst, ms): pass


def f(s):
    [i for i in s]
    print(s)
    print("---------------------")
 
if __name__=="__main__":
    s=RadioActiveSet((8,4,6,46,5,555, 9.276,565,966666,665) ); print(s); print("---------------")
    for i in range(100): f(s)

    