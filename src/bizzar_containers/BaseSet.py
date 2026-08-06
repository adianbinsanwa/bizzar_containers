from __future__ import annotations
from typing import Any, Callable, Iterator, Hashable;   from itertools import pairwise as prws
#from dataclasses import dataclass, field
from BaseModels import docs as bm_docs, ManipulatorSet as ms, SizedType as st, TypedType as tt, MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt
from SubModels import docs as sm_docs, IndexedType as it, UnaryGraphType as ugt, BinaryGraphType as bgt, TrinaryGraphType as tgt



##########-set families-##########


class LifetimeSet(lt, ms):   
    __doc__=bm_docs['lifetime']
    
    def from_itetable(self, res): return type(self)(self._manipulator.lifespan, res)
    
    def add(self, value: Hashable, lifespan=None):
        if value in self: return
        if lifespan is None: super().add(value); return
        obj._values.add(value); self._manipulator.items[value]=self._lifespan_is_valid(lifespan)
       
        
class IndexedSet[T](it, ms[T]):
    __doc__=sm_docs['indexed']
     
    def order(self) ->tuple[T]: return tuple(self._manipulator.key_order)
        
        
class RadioActiveSet(rat, ms):
    __doc__=bm_docs['radioactive']
    
    def _del(self, target): self.discard(target)
        
        
class SizedSet(st, ms):
    __doc__=bm_docs['sized']
    
    def from_iterable(self, res): return type(self)(self.capacity, res)
    

class TypedSet(tt, ms):
    __doc__=bm_docs['typed']
    
    def from_iterable(self, res): return type()(self.allowed_types, res)
    
    
class MemorySizedSet(mst, ms):
    __doc__=bm_docs['memorysized']
    
    def from_iterable(self, res): return type(self)(self.capacity, res)


class UnaryGraphSet(ugt, ms):
    __doc__=sm_docs['unary']
                
        
class BinaryGraphSet(bgt, ms):
    __doc__=sm_docs['binary']
    
    
class TrinaryGraphSet(tgt, ms):
    __doc__=sm_docs['trinary']
 

def f(s):
    print([i for i in s])
    print(s)
    print("---------------------")

def f1(s, funcs: Itreable[Callable[[Any], None] ]):
    for i in funcs:
        i(s); print(s, f"{s.metadata()=}", end="\n\n")#, sep="\n\n-------------------------------------\n\n" )


if __name__=="__main__":
    r=UnaryGraphSet(range(10), links={a:{b} for a,b in prws([0,2,4,6,8])}|{a:{b} for a,b in prws([1,3,5,7,9])})
    print(r.__doc__)
    f1(r, [lambda x: None, lambda x: x.new_link({0:{1}}), lambda x: x.remove(9) ])
    