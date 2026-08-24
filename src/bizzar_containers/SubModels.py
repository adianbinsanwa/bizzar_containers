from __future__ import annotations
from typing import Any, Iterator, Iterable, Hashable, Optional, Callable
from dataclasses import dataclass, field;   from types import MappingProxyType as mpt
from .BaseModels import T, missing, prtl, ManipulatorSet as mset

dtc=prtl(dataclass, slots=True, eq=False)


class LinkError(Exception): pass

@dtc
class BaseNodeM:
    links: dict[Hashable, set[Hashable] ]=field(init=False, default_factory=dict)
    
    def _error(self, a, b):
        if (is_a:= a not in self.links) or b not in self.links: raise KeyError(a if is_a else b)
        elif a==b: raise LinkError(f"cannot link '{a}' to itself")
    
    def metadata(self) ->mpt[Hashable, frozenset[Hashable] ]: return mpt({k:frozenset(v) for k,v in self.links.items()})
    
    def create(self, obj): copy=obj._values.copy(); obj._values.clear(); obj._set(copy)
    
        
@dtc        
class UnaryNodeM(BaseNodeM):
    parent_map: dict[Hashable, set[Hashable] ]=field(init=False, default_factory=dict)
    hub: set[Hashable]=field(init=False, default_factory=set)
    
    def _is_reachable_from(self, source: set[Hashable], target: Hashable):
        if target in source: return True
        for i in source:
            if (not (has_seen:= i in self.hub) ) and (not self._is_reachable_from(self.links[i], target) ):
                if len(self.parent_map[i]) > 1: self.hub.add(i)
            elif has_seen: continue
            else: return True
        return False
        
    def new_link(self, a: Hashable, b: Hashable):
        self._error(a,b)
        if self._is_reachable_from(self.links[b], a): raise LinkError(f"cannot link '{a}' to '{b}' where '{b}' is a super-parent of '{a}'")
        self.links[a].add(b); self.parent_map[b].add(a); self.hub.clear()
    
    def parents(self) ->mpt[Hashable, frozenset[Hashable] ]: return mpt({k:frozenset(v) for k,v in self.parent_map.items()})
    
    def set(self, obj, base_action: Callable[[], None], value, key=missing): val=value if key is missing else key; base_action(); self.links.setdefault(val, set() ); self.parent_map.setdefault(val, set() )
    
    def delete(self, obj, base_action: Callable[[], None], value):
        for i in self.parent_map.pop(value): self.links[i].remove(value)
        for i in (childs:= self.links.pop(value) ): self.parent_map[i].remove(value)
        for i in childs: obj._del(i)
        base_action()
    
     
class BinaryNodeM(BaseNodeM):
    def _bare_connect(self, a: Hashable, b: Hashable): self.links[a].add(b); self.links[b].add(a)
    
    def new_link(self, a: Hashable, b: Hashable): self._error(a, b); self._bare_connect(a, b)
      
    def set(self, obj, base_action: Callable[[], None], value, key=missing): val=value if key is missing else key; base_action(); self.links.setdefault(val, set() )
    
    def delete(self, obj, base_action: Callable[[], None], value):
        for i in (childs:= self.links.pop(value) ): self.links[i].remove(value)
        for i in childs: obj._del(i)
        base_action()
          

class TrinaryNodeM(BinaryNodeM):
    def new_link(self, a: Hashable, b: Hashable):
        self._error(a, b)
        for n1 in (self.links[a] | {a}):
            for n2 in (self.links[b] | {b}): self._bare_connect(n1, n2)


@dtc
class IndexedM:
    key_order: list[Hashable]=field(init=False, default=None)
    
    def create(self, obj): self.key_order=[i for i in obj]
        
    def set(self, obj, base_action: Callable[[], None], value: Any, key: Hashable|object=missing):
        if (target:= value if key is missing else key) not in self.key_order: self.key_order.append(target)
        base_action()
   
    def delete(self, obj, base_action: Callable[[], None], key: Hashable):
        if key in self.key_order: self.key_order.pop(self.key_order.index(key) )
        base_action()


@dtc
class IndexedFrozenM:
    key_order: tuple[Hashable]=field(init=False, default=None)
    
    def create(self, obj): self.key_order=tuple(i for i in obj)


##########-invariant types-##########    


class BaseGraphType:
    def __init__(self, *args, links: dict[Hashable, Iterable[Hashable] ]={}, **kwargs): super().__init__(self._getM(), *args, **kwargs); self.new_link(links)
    
    def _set(self, val):
        if isinstance(self, mset): self.update(val); return
        for k,v in val.items(): self[k]=v 
    
    def _del(self, val): getattr(self, 'discard' if isinstance(self, mset) else 'pop')(val)
    
    def new_link(self, links: dict[Hashable, Iterable[Hashable] ]):
        for parent, childs in links.items():
            for child in childs: self._manipulator.new_link(parent, child)
    
    def metadata(self) ->mpt[Hashable, set[Hashable] ]: return self._manipulator.metadata()


class UnaryGraphType(BaseGraphType):
    def _getM(self): return UnaryNodeM()
    
    def parents(self) ->mpt[Hashable, frozenset[Hashable] ]: return self._manipulator.parents()
    
    
class BinaryGraphType(BaseGraphType):
    def _getM(self): return BinaryNodeM()
    

class TrinaryGraphType(BaseGraphType):
    def _getM(self): return TrinaryNodeM()
    

class IndexedType:
    def __init__(self, *args, **kwargs): super().__init__(IndexedM(), *args, **kwargs)
        
        
class IndexedFrozenType: 
    def __init__(self, *args, **kwargs): super().__init__(IndexedFrozenM(), *args, **kwargs)
 

if __name__=="__main__":
    ...
    
 