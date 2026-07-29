from __future__ import annotations
from typing import Any, Callable
from dataclasses import dataclass as dtc, field;   from random import randint as rint
from .BaseModels import ManipulatorList as ml, SizedType as st, TypedType as tt, MemorySizedType as mst, LifetimeType as lt



@dtc(slots=True)
class HideSeekM:
    hider: int=field(init=False, default=0)
    
    def _jump(self, size: int): self.hider=rint(0, size)
    
    def create(self, obj): self._jump(len(obj) )
    
    def get(self, obj, base_action: Callable[[], Any], key: int) ->Any:
        i=base_action()
        if key==self.hider: del obj._values[key]; self._jump(len(obj))
        return i


class HideSeekList(ml):
    """HideSeekList implements the base idea of hide→seek. it has an internal pointer=the hider.
       on each (non iterative) element access it'll throw the pointer to a random spot.
       if the next access index ==hider's pos → it'll pop that item before repeating the cycle until the list is empty
    """
    
    def __init__(self, *args, **kwargs): super().__init__(HideSeekM(), *args, **kwargs)
        

class LifetimeList(lt, ml): pass
    

class SizedList(st, ml): pass
    

class TypedList(tt, ml): pass
    
    
class MemorySizedList(mst, ml): pass
    


if __name__=="__main__":
    d=LifetimeList(1,(8,56,66,7,6,6) )
    #print(d[2])
    print(d.check_lifespan(2))
    print(isinstance(d, ml)) 