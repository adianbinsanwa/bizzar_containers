from __future__ import annotations
from typing import Any, Iterator, Optional, Callable
from dataclasses import dataclass, field;   from random import randint as rint
from .BaseModels import Dead, ManipulatorList as ml, SizedType as st, TypedType as tt, MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt
from .SubModels import T

dtc=prtl(dataclass, slots=True, eq=False)


@dtc
class LifetimeM:
    lifespan: int
    items: list[int]=field(init=False, default=None)
    
    def _del(self, obj, it: Iterable[Any]):
        dead=set()
        for i in it: 
            self.items[i]-=1
            if self.items[i] is Dead: dead.add(i)
        for i in sorted(dead, reverse=True): del obj[i]
        
    def create(self, obj): self.items=[self.lifespan]*len(obj)
    
    def iterate(self, obj, base_action: Callable[[], T]) ->T: it=iter(obj._values.copy() ); self._del(obj, range(len(obj) ) ); return it
    
    def get(self, obj, base_action: Callable[[], T], key: int|slice) ->T: val=base_action(); self._del(obj, range(*key.indices(len(obj) ) ) if isinstance(key, slice) else (key,) ); return val
    
    def set(self, obj, base_action: Callable[[], None], value, key: int|slice): base_action(); self.items[key]=([self.lifespan]*len(value) ) if isinstance(key, slice) else self.lifespan
  #same  
    def delete(self, obj, base_action: Callable[[], None], key: int|slice): base_action(); del self.items[key]


@dtc
class HideSeekM:
    hider: int=field(init=False, default=0)
    
    def _jump(self, size: int): self.hider=rint(0, size)
    
    def create(self, obj): self._jump(len(obj) )
    
    def get(self, obj, base_action: Callable[[], T], key: int) ->T:
        i=base_action()
        if key==self.hider: del obj._values[key]; self._jump(len(obj) )
        return i
    
    def delete(self, obj, base_action: Callable[[], None], key: int|slice): base_action(); self._jump(len(obj) )


class HideSeekList(ml):
    """HideSeekList implements the base idea of hide→seek. it has an internal pointer=the hider.
       on each (non iterative) element access it'll throw the pointer to a random spot.
       if the next access index ==hider's pos → it'll pop that item before repeating the cycle until the list is empty
    """
    
    def __init__(self, *args, **kwargs): super().__init__(HideSeekM(), *args, **kwargs)
        
        
class LifetimeList(lt, ml):
    def _getM(self, lifespan): return LifetimeM(lifespan)
    
    def append(self, value, lifespan: Optional[int]=None):
        if lifespan is None: super().append(value)
        else: self._values.append(value); self._manipulator.items.append(self._lifespan_is_valid(lifespan) )
    
    def insert(self, index: int, value, lifespan: Optional[int]=None):
        if lifespan is None: super().insert(index, value)
        else: self._values.insert(index, value); self._manipulator.items.insert(index, self._lifespan_is_valid(lifespan) )
    
    
      
class RadioActiveList(rat, ml): pass
    

class SizedList(st, ml): pass
    

class TypedList(tt, ml): pass
    
    
class MemorySizedList(mst, ml): pass
    


if __name__=="__main__":
    d=RadioActiveList((8,56,66,7,6,6,665,44,877,44) )
    print(d[2])
    for r in range(90):
        for i in d: print(i)
    print(list(d), d)