from __future__ import annotations
from typing import Any, Callable, Iterator, Hashable
from dataclasses import dataclass as dtc, field
from .BaseModels import ManipulatorSet as ms, SizedType as st, TypedType as tt, MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt
from .SubModels import IndexedType as it

##########-set families-##########

class LifetimeSet(lt, ms):    
    def add(self, value: Hashable, lifespan=None):
        if value in self: return
        if lifespan is None: super().add(value); return
        obj._values.add(value); self._manipulator.items[value]=self._lifespan_is_valid(lifespan)
       
        
class IndexedSet[T](it, ms[T]):
    """IndexedSet keeps track of item order while keeping set invariants like:- fast lookups, unique values"""
    
    def order(self) ->tuple[T]: return tuple(self._manipulator.key_order)
        
        
class RadioActiveSet(rat, ms):
    def _del(self, target): self.discard(target)
    

class SizedSet(st, ms): pass
    

class TypedSet(tt, ms): pass
    
    
class MemorySizedSet(mst, ms): pass


def f(s):
    print([i for i in s])
    print(s)
    print("---------------------")
 
if __name__=="__main__":
    s=RadioActiveSet((8,4,6,46,5,555, 9.276,565,966666,665) ); print(s); print("---------------"); s.update((99, 2002, 2209))
    for i in range(10): f(s)

    