from __future__ import annotations
from typing import Any, Callable, Iterator, Hashable
#from dataclasses import dataclass, field
from .BaseModels import ManipulatorSet as ms, SizedType as st, TypedType as tt, MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt
from .SubModels import IndexedType as it, UnaryGraphType as ugt, BinaryGraphType as bgt, TrinaryGraphType as tgt



##########-set families-##########


class UnaryGraphSet(ugt, ms):
    def _set(self, val): self.update(val)
    
    def _del(self, val): self.discard(val)
    
    def add(self, value: Hashable, /, *, links: dict[Hashable, Iterable[Hashable] ]={}): super().add(value); self.new_link(links)
    
    def update(self, value: Hashable, /, *, links: dict[Hashable, Iterable[Hashable] ]={}): super().update(value); self.new_link(links)
    

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
        
        
class BinaryGraphSet(bgt, UnGraphSet): pass
    
    
class TrinaryGraphSet(tgt, UnGraphSet): pass    
 
    
class SizedSet(st, ms): pass
    

class TypedSet(tt, ms): pass
    
    
class MemorySizedSet(mst, ms): pass


def f(s):
    print([i for i in s])
    print(s)
    print("---------------------")
 
if __name__=="__main__":
    s=UnGraphSet(range(10), links={0:{2}, 2:{4}, 4:{6}, 6:{8}} )
    print(s, f"{s.metadata()=}", f"{s.parents()=}", sep="\n\n-------------------------------------\n\n" )
    s.remove(0)
    print(s, f"{s.metadata()=}", f"{s.parents()=}", sep="\n\n-------------------------------------\n\n" )

    