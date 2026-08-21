from __future__ import annotations
from typing import Any, Self, TypeVar, Iterable, Iterator, Callable, Hashable;   from types import UnionType as ut, MappingProxyType as mpt
from dataclasses import dataclass, field;   from pympler.asizeof import asizeof;  from random import random as r;   from functools import partial as prtl
from collections.abc import Sequence as fs, Set as fset, Mapping as fm, MutableSequence as ms, MutableSet as mset, MutableMapping as mm
from .documents import docs

dtc=prtl(dataclass, slots=True, eq=False)
Typed_simplifier=lambda x: x if isinstance(x, tuple) else ((x,) if isinstance(x, type) else tuple(x) )
T=TypeVar("T")
missing=object()
Dead=0
   
def Typed_simplifier(x: tuple|type|ut):
    try: isinstance(909, x); return x
    except TypeError as e: raise TypeError("invalid 'allowed types'. must be a type, a tuple of types or a union") from None
               
  
##########-base models-##########

@dtc
class ManipulatorProtocol:
    __doc__=docs["protocol"]
    
    def create(self, obj) ->None: print("create")
        
    def iterate(self, obj, base_action: Callable[[], T]) ->T: print("iterate"); return base_action()
        
    def get(self, obj, base_action: Callable[[] ,T], key) ->T: print("get", key); return base_action()
        
    def set(self, obj, base_action: Callable[[], None], value, key=None): print("set", value, key); base_action()
        
    def insert(self, obj, base_action: Callable[[], None], value, key=None) ->None: print("insert", value, key); base_action() 
        
    def delete(self, obj, base_action: Callable[[], None], key): print("delete", key); base_action()
    

class BaseContainerType[T]:
    #create, iterate
    __slots__=("_values", "_manipulator")
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator): self._manipulator=manipulator; self._notify("create")
    
    #base container ops
    def __eq__(self, other): return self._values == other if not hasattr(other, '_values') else other._values
    
    def __repr__(self) ->str: r=repr(self._values); return f"{type(self).__name__}({r if isinstance(self._values, (list, set, dict, tuple) ) else r[r.index('(')+1:-1]})"
    
    def __iter__(self) ->Iterator[T]: return self._notify("iterate", default= lambda: iter(self._values) )
    
    def __contains__(self, other: Any) ->bool: return other in self._values
        
    def __len__(self) ->int: return len(self._values)

    #protected ops  
    def _notify(self, action_taken: str, /, *data, default: Optional[Callable[[], Any] ]=None) ->Any:
        if not hasattr(self._manipulator, action_taken): return default() if callable(default) else None
        f=getattr(self._manipulator, action_taken); return f(self, default, *data) if data else (f(self, default) if callable(default) else f(self) )
        
            
##########-Manipulator family-##########

#immutables
class ManipulatorTuple[T](BaseContainerType[T], fs):
    __slots__=("_normalize_slice",)
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator, it: Iterable[T]=(), /, *, normalize_slice: bool =False): self._values, self._normalize_slice=tuple(it), normalize_slice; super().__init__(manipulator)
    
    def __getitem__(self, key) ->Any:
        if not self._normalize_slice and not isinstance(key, slice): return self._notify("get", key, default=lambda: self._values[key])
        return list(self[i] for i in range(*key.indices(len(self) ) ) )
    

class ManipulatorFrozenDict[T, U](BaseContainerType[T], fm):
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator, it: Iterable[tuple[T, U] ]=(), /, **kwargs): self._values=mpt({k:v for k,v in (dict(it)|kwargs).items()} ); super().__init__(manipulator)
    
    def __getitem__(self, key) ->Any: return self._notify("get", key, default=lambda: self._values[key])
    
class ManipulatorFrozenSet[T](BaseContainerType[T], fset):
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator, it: Iterable[Hashable]=() ): self._values=frozenset(it); super().__init__(manipulator)
    

#mutables
class ManipulatorList[T](BaseContainerType[T], ms):
    __slots__=("_normalize_slice",)
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator, it: Iterable[T]=(), /, *, normalize_slice: bool =False): self._values, self._normalize_slice=list(it), normalize_slice; super().__init__(manipulator)
    
    def __getitem__(self, key) ->Any:
        if not self._normalize_slice and not isinstance(key, slice): return self._notify("get", key, default=lambda: self._values[key])
        return [self[i] for i in range(*key.indices(len(self) ) )]
    
    def __setitem__(self, key, value) ->None: 
        if not self._normalize_slice and not isinstance(key, slice): self._notify("set", value, key, default=lambda: self._values.__setitem__(key, value) ); return
        for i, v in zip(range(*key.indices(len(self) ) ), value): del self[i]; self.insert(i, v)
    
    def __delitem__(self, key) ->None: 
        if not self._normalize_slice and not isinstance(key, slice): self._notify("delete", key, default=lambda: self._values.__delitem__(key) ); return
        for i in range(*key.indices(len(self) ) ): del self[i]
    
    def insert(self, index: int, value): 
        if hasattr(self._manipulator, "insert"): self._manipulator.insert(self, lambda: self._values.insert(index, value), value, index)
        else: self._notify("set", value, index, default=lambda: self._values.insert(index, value) )


class ManipulatorSet[T](BaseContainerType[T], mset):
    #set
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator, it: Iterable[Hashable]=() ): self._values=set(it); super().__init__(manipulator)
    
    def add(self, value: Hashable): 
        if value in self: return
        elif hasattr(self._manipulator, "insert"): self._manipulator.insert(self, lambda: self._values.add(value), value)
        else: self._notify("set", value, default=lambda: self._values.add(value) )
        
    def update(self, it: Iterable[Hashable]):
        for i in it: self.add(i)
    
    def discard(self, other: Hashable): 
        if other in self: self._notify("delete", other, default=lambda: self._values.discard(other) )


class ManipulatorDict[T, U](BaseContainerType[T], mm):
    __doc__=docs['manipulator']
    
    def __init__(self, manipulator, it: Iterable[tuple[T, U] ]=(), /, **kwargs): self._values=dict(it)|kwargs; super().__init__(manipulator)
    
    def __getitem__(self, key) ->Any: return self._notify("get", key, default=lambda: self._values[key])
    
    def __setitem__(self, key, value):
        if key not in self and hasattr(self._manipulator, "insert"): self._manipulator.insert(self, lambda: self._values.__setitem__(key, value), value, key)
        else: self._notify("set", value, key, default=lambda: self._values.__setitem__(key, value) )    
            
    def __delitem__(self, key) ->None: self._notify("delete", key, default=lambda: self._values.__delitem__(key) )
                
        
##########-Manipulators-##########


@dtc
class LifetimeM:
    lifespan: int
    items: dict[Hashable, int]=field(init=False, default=None)
    
    def create(self, obj): self.items={i:self.lifespan for i in obj._values}#; open_collector_slot(obj)
    
    def iterate(self, obj, base_action: Callable[[], T]) ->T:
        it=iter(obj._values.copy() )
        for i in obj._values:
            self.items[i]-=1
            if self.items[i] is Dead: getattr(obj, "pop" if isinstance(obj, md) else "discard")(i)
        return it
    
    def get(self, obj, base_action: Callable[[], T], key: Hashable) ->T:
        val=base_action(); self.items[key]-=1
        if self.items[key] is Dead: del obj[key]
        return val
        
    def set(self, obj, base_action: Callable[[], None], value: Any, key: object|Hashable=missing): base_action(); self.items.setdefault(value if key is missing else key, self.lifespan)
    
    def delete(self, obj, base_action: Callable[[], None], value: Hashable): base_action(); del self.items[value]


@dtc(frozen=True)
class SizedM:
    """SizedManipulator is a manipulator for SizedType conatiners"""
    
    min_size: int
    max_size: int
    
    def create(self, obj):
        if self.min_size > self.max_size: raise ValueError(f"min_size:-{self.min_size} must be less than or equal to max_size:-{self.max_size}")
        elif self.min_size < 0 or self.max_size < 0: raise ValueError("min_size and max_size must be non-negetive")
        self.delete(obj, lambda: None, None); self.set(obj, lambda: None, None)
            
    def set(self, obj, base_action: Callable[[], None], value, key: Optional[Hashable| int]=None):
        base_action()
        if len(obj) > self.max_size: raise OverflowError(f"maximum capacity violeted, limit:- {self.max_size}")
    
    def delete(self, obj, base_action: Callable[[], None], value):
        base_action()
        if len(obj) < self.min_size: raise OverflowError(f"minimum capacity violeted, limit:-{self.min_size}")
    @property
    def capacity(self) ->tuple[int, int]: return self.min_size, self.max_size


class MemorySizedM(SizedM):
    """MemorySizedManipulator is a manipulator for MemorySizedType conatiners."""
    
    def set(self, obj, base_action: Callable[[], None], value, key: Optional[Hashable| int]=None):
        base_action()
        if (asizeof(obj._values) - asizeof(type(obj._values)() ) ) > self.max_size: raise OverflowError(f"maximum memory capacity violeted, limit:- {self.max_size}")
    
    def delete(self, obj, base_action: Callable[[], None], value):
        base_action()
        if (asizeof(obj._values) - asizeof(type(obj._values)() ) ) < self.min_size: raise OverflowError(f"minimum memory capacity violeted, limit:-{self.min_size}")
            

@dtc(frozen=True)
class TypedM:
    """TypedManipulator is a manipulator for TypedType conatiners"""
    
    allowed_types: tuple[type]
    
    def create(self, obj):
        for i in obj: self.set(None, lambda: None, i)
    
    def set(self, obj, base_action, value, key: Optional[Hashable| int]=None):
        if type(value) not in self.allowed_types: raise TypeError(f"invalid value type, expected:-{' or '.join(f'{i.__name__}' for i in self.allowed_types)}, got:-'{type(value).__name__}'")
        base_action()


@dtc
class GroupM:
    groups: dict[str, Iterable[Any] ]=field(init=False, default_factory=dict)
    
    def delete(self, obj, base_action, key):
        base_action()
        for v in self.groups.values():
            if key in v: v.remove(key)
    

@dtc(frozen=True)
class RadioActiveM:   
    #def create(self, obj): open_collector_slot(obj)
    
    def iterate(self, obj, base_action: Callable[[], T]) ->T:
        rand=((r(), i) for i in obj._get() )
        if len(obj) > 0 and (r() >= (high:= max(rand, key=lambda x: x[0]) )[0] >= r() ): it=iter(obj._values.copy() ); obj._del(high[1]); return it
        return base_action()


##########-invariant types-##########    


class GroupType:
    def __init__(self, *args, **kwargs): super().__init__(GroupM(), *args, **kwargs); self._values=self._trackIndex(self._values)
    
    def _check_members(self, members):
        for i in members:
            if i >=len(self): raise IndexError(f"{type(self).__name__} index out of range")
    
    def _check_grp_not_exists(self, name):
        if name in self._get_groups: raise ValueError(f"cannot override existing group '{name}': use '.change()' to override a group")
    
    def _check_grp_exists(self, name):
        if name not in self._get_groups: raise ValueError(f"invalid group name: '{target}' notfound")
    @property
    def _get_groups(self): return self._manipulator.groups
    
    def discard_group(self, target):
        if target in self.groups: del self.manipulator.groups[target]
    
    def remove_group(self, target: str): self._error_for_nonexisting_grp(target); del self._get_groups[target]
    
    @property
    def groups(self) ->mpt[str, Iterable[Any] ]: return mpt(self._get_groups)
    
    def clear_groups(self): self._get_groups.clear()
 

class LifetimeType:
    def __init__(self, lifespan: int, *args, **kwargs): super().__init__(self._getM(self._lifespan_is_valid(lifespan) ), *args, **kwargs)
    
    def _lifespan_is_valid(self, n: int) ->int:
        if not isinstance(n, int): raise TypeError(f"invalid type '{type(n).__name__}'. must be an integer")
        elif n <= 0: raise ValueError("lifespan cannot be zero or negetive")
        return n
        
    def _getM(self, lifespan: int): return LifetimeM(lifespan)
 
    def get_lifespans(self) ->mpt[Hashable, int]: return mpt(self._manipulator.items)
   
    
class SizedType: 
    def __init__(self, size: tuple[int, int]|int, /, *args, **kwargs): super().__init__(self._getM(*(size if isinstance(size, tuple) else (0, size) ) ), *args, **kwargs)
    
    def _getM(self, *size): return SizedM(*size)
    @property
    def capacity(self) ->tuple[int, int]: return self._manipulator.capacity


class TypedType:
    def __init__(self, allowed_types: type|tuple[type], /, *args, **kwargs): super().__init__(TypedM(Typed_simplifier(allowed_types) ), *args, **kwargs) 
    @property
    def allowed_types(self): return self._manipulator.allowed_types


class RadioActiveType:
    def __init__(self, *args, **kwargs): super().__init__(RadioActiveM(), *args, **kwargs)
    
    def _del(self, target): del self[target]
    
    def _get(self): return self._values
    

class MemorySizedType(SizedType): 
    def _getM(self, *size): return MemorySizedM(*size)

     
if __name__=="__main__":
    ...
    

