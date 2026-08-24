from __future__ import annotations
from typing import Any, Self, Iterator, Optional, Callable
from dataclasses import dataclass, field;   from random import randint as rint
from .BaseModels import (T, prtl, Dead, docs,

ManipulatorList as ml, ManipulatorTuple as mt, SizedType as st, TypedType as tt,
MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt, GroupType as gt)

#from .SubModels import 

dtc=prtl(dataclass, slots=True, eq=False)


@dtc
class LifetimeM:
    lifespan: int
    items: list[int]=field(init=False, default=None)
    
    def _del(self, obj, it: Iterable[Any]):
        for i in it: 
            self.items[i]-=1
            if self.items[i] is Dead: del obj[i]
        
    def create(self, obj): self.items=[self.lifespan]*len(obj)
    
    def iterate(self, obj, base_action: Callable[[], T]) ->T: it=iter(obj._values.copy() ); self._del(obj, reversed(range(len(obj) ) ) ); return it
    
    def get(self, obj, base_action: Callable[[], T], key: int|slice) ->T: val=base_action(); self._del(obj, reversed(range(*key.indices(len(obj) ) ) ) if isinstance(key, slice) else (key,) ); return val
    
    def set(self, obj, base_action: Callable[[], None], value, key: int|slice): base_action(); self.items[key]=([self.lifespan]*len(value) ) if isinstance(key, slice) else self.lifespan
    
    def insert(self, obj, base_action: Callable[[], None], value, key: int|slice): base_action(); self.items.insert(key, self.lifespan)
    
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


##########-Manipulators-##########


class LifetimeList(lt, ml):
    __doc__=docs['lifetime']
    
    def _getM(self, lifespan): return LifetimeM(lifespan)
    
    def append(self, value, lifespan: Optional[int]=None):
        if lifespan is None: super().append(value)
        else: self._values.append(value); self._manipulator.items.append(self._lifespan_is_valid(lifespan) )
    
    def insert(self, index: int, value, lifespan: Optional[int]=None):
        if lifespan is None: super().insert(index, value)
        else: self._values.insert(index, value); self._manipulator.items.insert(index, self._lifespan_is_valid(lifespan) )
            
    
class HideSeekList(ml):
    """HideSeekList implements the base idea of hide→seek. it has an internal pointer=the hider.
       on each (non iterative) element access it'll throw the pointer to a random spot.
       if the next access index ==hider's pos → it'll pop that item before repeating the cycle until the list is empty
    """
    
    def __init__(self, *args, **kwargs): super().__init__(HideSeekM(), *args, **kwargs)
            
      
class RadioActiveList(rat, ml):
    __doc__=docs['radioactive']
    
    def _get(self): return range(len(self) )
    

class SizedList(st, ml):
    __doc__=docs['sized']
    

class TypedList(tt, ml):
    __doc__=docs['typed']
    
    
class MemorySizedList(mst, ml):
    __doc__=docs['memorysized']
    
    
class GroupTuple(gt, mt):
    __doc__=docs["group"]
    
    def _trackIndex(self, data): return data
    
    def new_groups(self, **groups) ->Self:
        for name, members in groups.items():
            self._check_grp_not_exists(name); self._check_members(members); self._manipulator.groups.setdefault(name, tuple(self[i] for i in members) )
        return self
        
    def change_members(self, target, new_members: Iterable[int]):
        self._check_grp_exists(target); self._check_members(new_members); self._manipulator.groups[target]=tuple(self[i] for i in new_members)
    
    

if __name__=="__main__":
    d=GroupTuple( (8,56,66,7,6,6,665,44,877,44) )
    d.new_group(name=(2,4,3,5,5) )

    print(d.groups)