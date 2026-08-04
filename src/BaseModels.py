from __future__ import annotations
from typing import Any, Self, Iterable, Iterator, Callable, Hashable;   from types import UnionType as ut
from dataclasses import dataclass, field;   from pympler.asizeof import asizeof;  from random import random as r
from collections.abc import MutableSequence as ms, MutableSet as mset, MutableMapping as mm

dtc=prtl(dataclass, slots=True, eq=False)
Typed_simplifier=lambda x: x if isinstance(x, tuple) else ((x,) if isinstance(x, type) else tuple(x) )
missing=object(); Dead=0

def Typed_simplifier(x: tuple|type|ut):
    try: isinstance(909, x); return x
    except TypeError as e: raise TypeError("invalid 'allowed types'. must be a type, a tuple of types or a union") from None
    
##########-base models-##########

@dtc
class ManiuatorProtocol:
    """BaseManipulatorProtocol is a blueprint for manipulator protocols
       there are five protocols:-
           create:- after instansiating the container "create" is called,
           iterate:- when iter() is called on the container "iterate" is called
           get:- when element accessing happens "get" is called
           set:- when setting a value happens "set" is called
           delete:- when deleting an element "delete" is called
       note:- if the manipulator doesn't implement the target protocol. it'll switch to a base_protocol instead.
            otherwise the manipulator is expected to handle the action.
    """
    
    def create(self, obj) ->None: pass
        
    def iterate(self, obj, base_action: Callable[[], T]) ->T: return base_action()
        
    def get(self, obj, base_action: Callable[[] ,T], key) ->T: return base_action()
        
    def set(self, obj, base_action: Callable[[], None], value, key=None): base_action()
        
    def delete(self, obj, base_action: Callable[[], None], key): base_action()
    

class KeyAccess:
    """This class is inherited by classes whom needs __getitem__, __setitem__, __delitem__"""
    #get, set, delete
        
    def __getitem__(self, key) ->Any: return self._notify("get", key, default=lambda: self._values[key])
        
    def __setitem__(self, key, value) ->None: self._notify("set", value, key, default=lambda: self._values.__setitem__(key, value) )
     
    def __delitem__(self, key) ->None: self._notify("delete", key, default=lambda: self._values.__delitem__(key) )
    

class BaseContainerType[T]:
    """BaseContainer/ManipulatorType is the base type for manipulator container family
       the manipulator given by the user controls the behavior when interacting with the container
    """#create, iterate

    __slots__=("_values", "_manipulator")
    
    def __init__(self, manipulator): self._manipulator=manipulator; self._notify("create")
    
    #base container ops
    def __repr__(self) ->str: return f"{type(self).__name__}({self._values})"
    
    def __iter__(self) ->Iterator[T]: return self._notify("iterate", default= lambda: iter(self._values) )
    
    def __contains__(self, other: Any) ->bool: return other in self._values
        
    def __len__(self) ->int: return len(self._values)

    #protected ops  
    def _notify(self, action_taken: str, /, *data, default: Optional[Callable[[], Any] ]=None) ->Any:
        if not hasattr(self._manipulator, action_taken): return default() if callable(default) else None
        f=getattr(self._manipulator, action_taken); return f(self, default, *data) if data else (f(self, default) if callable(default) else f(self) )
        
            
##########-Manipulator family-##########


class ManipulatorSet[T](BaseContainerType[T], mset):
    #set
    
    def __init__(self, manipulator, it: Iterable[Hashable]=() ): self._values=set(it); super().__init__(manipulator)
    
    def add(self, other: Hashable): 
        if other not in self: self._notify("set", other, default=lambda: self._values.add(other) )
    
    def update(self, it: Iterable[Hashable]):
        for i in it: self.add(i)
    
    def discard(self, other: Hashable): 
        if other in self: self._notify("delete", other, default=lambda: self._values.discard(other) )


class ManipulatorList[T](BaseContainerType[T], KeyAccess, ms):
    #set
    
    def __init__(self, manipulator, it: Iterable[T]=() ): self._values=list(it); super().__init__(manipulator)
    
    def insert(self, index: int, value): self._notify("set", value, index, default=lambda: self._values.insert(index, value) )
        
        
class ManipulatorDict[T, U](BaseContainerType[T], KeyAccess, mm):
    def __init__(self, manipulator, it: Iterable[tuple[T, U] ]=(), /, **kwargs): self._values=dict(it)|kwargs; super().__init__(manipulator);
    
    
##########-Manipulators-##########


@dtc
class LifetimeM:
    lifespan: int
    items: dict[Hashable, int]=field(init=False, default=None)
    
    def create(self, obj): self.items={i:self.lifespan for i in obj._values}
    
    def iterate(self, obj, base_action: Callable[[], T]) ->T:
        it=iter(obj._values.copy() )
        for i in obj._values:
            self.items[i]-=1
            if self.items[i] is Dead: d=getattr(obj, "pop" if isinstance(obj, md) else "discard"); d(i)
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


@dtc(frozen=True)
class RadioActiveM[T]:   
    def iterate(self, obj, base_action: Callable[[], T]) ->T:
        rand=((r(), i) for i in (obj._values if not isinstance(obj, ManipulatorList) else range(len(obj) ) ) )
        if len(obj) > 0 and (r() >= (high:= max(rand, key=lambda x: x[0]) )[0] >= r() ): it=iter(obj._values.copy() ); obj._del(high[1]); return it
        return base_action()


##########-invariant types-##########    


class LifetimeType:
    """LifetimeType containers's elements slowly decays after each access/iteration."""
    
    def __init__(self, lifespan: int, *args, **kwargs): super().__init__(self._getM(self._lifespan_is_valid(lifespan) ), *args, **kwargs)
    
    def _lifespan_is_valid(self, n: int) ->int:
        if not isinstance(n, int): raise TypeError(f"invalid type '{type(n).__name__}'. must be an integer")
        elif n <= 0: raise ValueError("lifespan cannot be zero or negetive")
        return n
        
    def _getM(self, lifespan: int): return LifetimeM(lifespan)
      
    def check_lifespan(self, target: int|Hashable) ->int: return self._manipulator.items[target]
   
    
class SizedType: 
    """Sized containers takes and enforces a size range.
       the container would never exceed this range.
    """
    
    def __init__(self, size: tuple[int, int]|int, /, *args, **kwargs): super().__init__(self._getM(*(size if isinstance(size, tuple) else (0, size) ) ), *args, **kwargs)
    
    def _getM(self, *size): return SizedM(*size)
    @property
    def capacity(self) ->tuple[int, int]: return self._manipulator.capacity


class MemorySizedType(SizedType): 
    """MemorySized containers is a variant of Sized containes. it counts capacity in memory bytes"""    
    
    def _getM(self, *size): return MemorySizedM(*size)


class TypedType:
    """Typed containers enforces value type within specific types."""
    
    def __init__(self, allowed_types: type|tuple[type], /, *args, **kwargs): super().__init__(TypedM(Typed_simplifier(allowed_types) ), *args, **kwargs) 
    @property
    def allowed_types(self): return self._manipulator.allowed_types


class RadioActiveType:
    """RadioActiveType enforces random decay. on each iteration there's a chance for an element to get removed(sometimes nothing happens too)"""
    
    def __init__(self, *args, **kwargs): super().__init__(RadioActiveM(), *args, **kwargs)
    
    def _del(self, target): del self[target]
   
     
if __name__=="__main__":
    ...
    

