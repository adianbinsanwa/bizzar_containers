from __future__ import annotations
from typing import Any, Self, Callable, Iterator, Hashable
#from dataclasses import dataclass, field
from .BaseModels import (docs, 

ManipulatorSet as ms, ManipulatorFrozenSet as mfs, SizedType as st, TypedType as tt,
MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt, GroupType as gt)

from .SubModels import IndexedFrozenType as ifs, IndexedType as it, UnaryGraphType as ugt, BinaryGraphType as bgt, TrinaryGraphType as tgt


##########-set families-##########


class LifetimeSet(lt, ms):   
    __doc__=docs['lifetime']
    
    def _from_itetable(self, res): return type(self)(self._manipulator.lifespan, res)
    
    def add(self, value: Hashable, lifespan=None):
        if value in self: return
        if lifespan is None: super().add(value); return
        obj._values.add(value); self._manipulator.items[value]=self._lifespan_is_valid(lifespan)
       
        
class IndexedSet[T](it, ms[T]):
    __doc__=docs['indexed']
     
    def order(self) ->tuple[T]: return tuple(self._manipulator.key_order)
        
        
class IndexedFrozenSet[T](ifs, mfs[T]):   
    __doc__=docs['indexed']
     
    def order(self) ->tuple[T]: return tuple(self._manipulator.key_order)        
        
        
class RadioActiveSet(rat, ms):
    __doc__=docs['radioactive']
    
    def _del(self, target): self.discard(target)
        
        
class SizedSet(st, ms):
    __doc__=docs['sized']
    
    def _from_iterable(self, res): return type(self)(self.capacity, res)
    

class TypedSet(tt, ms):
    __doc__=docs['typed']
    
    def _from_iterable(self, res): return type()(self.allowed_types, res)
    
    
class MemorySizedSet(mst, ms):
    __doc__=docs['memorysized']
    
    def _from_iterable(self, res): return type(self)(self.capacity, res)
    

class UnaryGraphSet(ugt, ms):
    __doc__=docs['unary']
                
        
class BinaryGraphSet(bgt, ms):
    __doc__=docs['binary']
    
    
class TrinaryGraphSet(tgt, ms):
    __doc__=docs['trinary']



class GroupSet(gt, ms):
    __doc__=docs["group"]
    
    def _trackIndex(self, data): return IndexedSet(data)
    
    def new_groups(self, **groups) ->Self:
        for name, members in groups.items():
            self._check_grp_not_exists(name); self._check_members(members); self._get_groups.setdefault(name, set(self.order()[i] for i in members) )
        return self
        
    def change_members(self, target, new_members: Iterable[int]):
        self._check_grp_exists(target); self._check_members(new_members); self._get_groups[target]=set(self.order()[i] for i in new_members)
    
    def add_members(self, target: str, new_nembers: Iterable[int]):
        self._check_grp_exists(target); self._check_members(new_members); self._get_groups[target].update(self.order()[i] for i in new_members)
    
    def free_group(self, target: str): self._error_for_nonexisting_grp(target); self._get_groups[target].clear() 
    
    def order(self) ->tuple[T]: return tuple(self._values._manipulator.key_order)            
     

class GroupFrozenSet(gt, mfs):
    __doc__=docs["group"]
    
    def _trackIndex(self, data): return IndexedFrozenSet(data)
    
    def new_groups(self, **groups) ->Self:
        for name, members in groups.items():
            self._check_grp_not_exists(name); self._check_members(members); self._get_groups.setdefault(name, frozenset(self.order()[i] for i in members) )
        return self
        
    def change_members(self, target, new_members: Iterable[int]):
        self._check_grp_exists(target); self._check_members(new_members); self._get_groups[target]=frozenset(self.order()[i] for i in new_members)
    
    def order(self) ->tuple[T]: return tuple(self._values._manipulator.key_order)        
    



def f(s):
    print([i for i in s])
    print(s)
    print("---------------------")

def f1(s, funcs: Itreable[Callable[[Any], None] ]):
    for i in funcs:
        i(s); print(s, f"{s.metadata()=}", end="\n\n")#, sep="\n\n-------------------------------------\n\n" )


if __name__=="__main__":
    r=GroupFrozenSet("1234567890")
    print(r, r.groups)
    