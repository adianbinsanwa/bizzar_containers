from __future__ import annotations
from typing import Any, Self, Iterable, Iterator, Callable, Hashable
from dataclasses import dataclass as dtc, field;   from pympler.asizeof import asizeof
from collections.abc import MutableSequence as ms, MutableSet as mset, MutableMapping as mm

Typed_simplifier=lambda x: x if isinstance(x, tuple) else ((x,) if isinstance(x, type) else tuple(x) )
Lifetime_simplifier=lambda x, s: s._values[x] if isinstance(s, ms) else x
    

##########-base models-##########

@dtc(slots=True)
class BaseManiuatorProtocol:
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
        
    def iterate(self, obj, base_action) ->Iterator[Any]: return base_action()
        
    def get(self, obj, base_action, key) ->Any: return base_action()
        
    def set(self, obj, base_action, value, key=None): base_action()
        
    def delete(self, obj, base_action, key): base_action()
    

class KeyAccess:
    """This class is inherited by the classes whom need __getitem__, __setitem__, __delitem__"""
    #get, set, delete
    
    
    def __getitem__(self, key): return self._notify("get", key, default=lambda: self._values[key])
        
    def __setitem__(self, key, value): self._notify("set", value, key, default=lambda: self._values.__setitem__(key, value) )
     
    def __delitem__(self, key): self._notify("delete", key, default=lambda: self._values.__delitem__(key) )
    

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


class ManipulatorDict[T, U](BaseContainerType[T], KeyAccess, mm):
    def __init__(self, manipulator, it: Iterable[tuple[T, U] ]=(), /, **kwargs): self._values=dict(it)|kwargs; super().__init__(manipulator);
    

class ManipulatorList[T](BaseContainerType[T], KeyAccess, ms):
    #pre_set
    #post_set
    
    def __init__(self, manipulator, it: Iterable[T]=() ): self._values=list(it); super().__init__(manipulator)
    
    def insert(self, index: int, value): self._notify("set", value, index, default=lambda: self._values.insert(index, value) )
    
    
class ManipulatorSet[T](BaseContainerType[T], mset):
    #pre_set
    #post_set
    
    def __init__(self, manipulator, it: Iterable[Hashable]=() ): self._values=set(it); super().__init__(manipulator)
    
    def add(self, other: Hashable): self._notify("set", other, default=lambda: self._values.add(other) )
    
    def discard(self, other: Hashable): 
        if other in self: self._notify("delete", other, default=lambda: self._values.discard(other) )


##########-Manipulators-##########


@dtc(slots=True, frozen=True)
class SizedM:
    """SizedManipulator is a manipulator for SizedType conatiners"""
    
    min_size: int
    max_size: int
    
    def create(self, obj):
        if self.min_size > self.max_size: raise ValueError(f"min_size:-{self.min_size} must be less than or equal to max_size:-{self.max_size}")
        elif self.min_size < 0 or self.max_size < 0: raise ValueError("min_size and max_size must be non-negetive")
        self.delete(obj, lambda: None, None); self.set(obj, lambda: None, None)
            
    def set(self, obj, base_action, value, key=None):
        base_action()
        if len(obj) > self.max_size: raise OverflowError(f"maximum capacity violeted, limit:- {self.max_size}")
    
    def delete(self, obj, base_action, value):
        base_action()
        if len(obj) < self.min_size: raise OverflowError(f"minimum capacity violeted, limit:-{self.min_size}")
    @property
    def capacity(self): return self.min_size, self.max_size


@dtc(slots=True, frozen=True)
class MemorySizedM(SizedM):
    """MemorySizedManipulator is a manipulator for MemorySizedType conatiners."""
    
    def set(self, obj, base_action, value):
        base_action()
        if (asizeof(obj._values) - asizeof(type(obj._values)() ) ) > self.max_size: raise OverflowError(f"maximum memory capacity violeted, limit:- {self.max_size}")
    
    def delete(self, obj, base_action, value):
        base_action()
        if (asizeof(obj._values) - asizeof(type(obj._values)() ) ) < self.min_size: raise OverflowError(f"minimum memory capacity violeted, limit:-{self.min_size}")
            

@dtc(slots=True, frozen=True)
class TypedM:
    """TypedManipulator is a manipulator for TypedType conatiners"""
    
    allowed_types: tuple[type]
    
    def create(self, obj):
        for i in obj: self.set(None, lambda: None, i)
    
    def set(self, obj, base_action, value, key=None):
        if type(value) not in self.allowed_types: raise TypeError(f"invalid value type, expected:-{' or '.join(f'{i.__name__}' for i in self.allowed_types)}, got:-'{type(value).__name__}'")
        base_action()


@dtc(slots=True)
class LifetimeM:
    """LifetimeManipulator is a manipulator for LifetimeType containers. it tracks the elements's lifespan"""
    
    lifespan: int
    items: dict[Any, int]=field(init=False, default=None)
    
    def __post_init__(self):
        if not isinstance(self.lifespan, int): raise TypeError(f"invalid type '{type(self.lifespan).__name__}'. must be an integer")
        elif self.lifespan < 0: raise ValueError("lifespan must be non-negetive")
    
    def create(self, obj): self.items=dict.fromkeys(obj._values, self.lifespan)
        
    def iterate(self, obj, base_action):
        copy=obj._values.copy()
        for i in self.items:
            self.items[i]-=1
            if self.items[i] <= 0: obj.pop(i)
        self._cleanup(obj); return iter(copy)
    
    def get(self, obj, base_action, key):
        copy=obj._values.copy(); self.items[Lifetime_simplifier(key, obj)]-=1
        if self.items[Lifetime_simplifier(key, obj)]<=0: obj.pop(k)
        return copy[key]
    
    def set(self, obj, base_action, value, key): self.items.setdefault(Lifetime_simplifier(key, obj), self.lifespan); base_action()    
     
    def delete(self, obj, base_action, key): self.items.pop(Lifetime_simplifier(key, obj) ); base_action()
        
    
##########-Universal invariants-##########    
    
    
class SizedType: 
    """Sized containers takes and enforces a size range.
       the container would never exceed this range.
    """
    
    def __init__(self, size: tuple[int, int]|int, /, *args, **kwargs): super().__init__(SizedM(*size if isinstance(size, tuple) else (0, size) ), *args, **kwargs)
    @property
    def capacity(self): return self._manipulator.capacity


class MemorySizedType: 
    """MemorySized containers is a variant of Sized containes. it counts capacity in memory bytes"""    
    
    def __init__(self, size: tuple[int, int], /, *args, **kwargs): super().__init__(MemorySizedM(*size if isinstance(size, tuple) else (0, size) ), *args, **kwargs)
    @property
    def capacity(self): return self._manipulator.capacity


class TypedType:
    """Typed containers enforces value type within specific types."""
    
    def __init__(self, allowed_types: type|tuple[type], /, *args, **kwargs): super().__init__(TypedM(Typed_simplifier(allowed_types) ), *args, **kwargs) 
    @property
    def allowed_types(self): return self._manipulator.allowed_types


class LifetimeType:
    """LifetimeType containers's elements slowly decays after each access, iteration."""
    def __init__(self, lifespan: int, /, *args, **kwargs): super().__init__(LifetimeM(lifespan), *args, **kwargs)
    
    def check_lifespan(self, key): return self._manipulator.items[key if not isinstance(self, ManipulatorList) else self._values[key] ]


if __name__=="__main__":
    ...
    

