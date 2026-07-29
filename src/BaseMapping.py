from __future__ import annotations
from typing import Any, Hashable, Callable
from dataclasses import dataclass as dtc, field;   from types import MappingProxyType as mpt
from .BaseModels import Typed_simplifier as ts, ManipulatorDict as md, SizedType as st, MemorySizedType as mst, LifetimeType as lt

##########-Manipulators-##########

@dtc(slots=True)
class DualValueM:
    extra_vals: dict[Any, Any]=field(init=False, default=None)
        
    def create(self, obj): self.extra_vals={i:None for i in obj}
        
    def set(self, obj, base_action, value, key): base_action(); self.extra_vals.setdefault(key, None)
        
    def delete(self, obj, base_action, key): base_action(); self.extra_val.pop(key)
    

@dtc(slots=True)
class QuantumM:
    links: dict[Any, set[Any] ]=field(init=False, default_factory=dict)
    
    def create(self, obj): self.links={i:set() for i in obj}
    
    def get(self, obj, base_action, key) ->Any: ...
    
    def set(self, obj, base_action, value, key): self.links.setdefault(key, set() ); base_action()
    
    def delete(self, obj, base_action, key): self.links.pop(key); base_action()
    
    def entange(self, a, b): ...
    
    
@dtc(slots=True, frozen=True)
class TypedM:
    allowed_keys: tuple[type]
    allowed_values: tuple[type]
    
    def create(self, obj):
        for k,v in obj.items(): self.set(None, lambda: None, k, v)
    
    def set(self, obj, base_action, value, key):
        if type(key) not in self.allowed_keys: raise TypeError(f"invalid key type, expected:-{' or '.join(f'{i.__name__}' for i in self.allowed_keys)}, got:-'{type(key).__name__}'")
        elif type(value) not in self.allowed_values: raise TypeError(f"invalid value type, expected:-{' or '.join(f'{i.__name__}' for i in self.allowed_values)}, got:-'{type(value).__name__}'")
        base_action()
        

@dtc(slots=True)
class IndexedM:
    key_order: list[Hashable]=field(init=False, default=None)
    
    def create(self, obj): self.key_order=[i for i in obj]
        
    def set(self, obj, base_action, value, key):
        if key not in self.key_order: self.key_order.append(key)
        base_action()
   
    def delete(self, obj, base_action, key): base_action(), self.key_order.pop(self.key_order.index(key) )
    

@dtc(slots=True)
class CanonicalM:
    checker: Callable[[Any, Any], bool]
    
    def create(self, obj):
        d=obj._values.copy(); obj._values.clear()
        for k,v in d.items(): obj[k]=v
    
    def set(self, obj, base_action, value, key) ->bool:
        for k,v in obj.items():
            if self.checker(value, v): obj._values[key]=v; break
        else: base_action()

@dtc(slots=True)
class FixSizedM:
    size: int=field(init=False, default=None)
    
    def create(self, obj): self.size=len(obj)
    
    def set(self, obj, base_action, value, key):
        if key in obj: base_action()
        elif value in obj.values():
            for k,v in obj.items():
                if v is value: obj._values.pop(k); break
            base_action()  
        else: raise SizedTypeError(f"cannot modify a {type(obj).__name__}'s size")
    
    def delete(self, obj, base_action, key): raise SizedTypeError(f"cannot modify a {type(obj).__name__}'s size")

##########-dict families-##########

class IndexedDict[T, U](md[T, U]):
    """IndexedDict allowes key, value, item access using index"""
    
    def __init__(self, *args, **kwargs): super().__init__(IndexedM(), *args, **kwargs)
        
    @property
    def indexes(self) ->tuple[T]: return tuple(self._manipulator.key_order)
     
    def value_at(self, index) ->U: return self[self.key_at(index)]
    
    def item_at(self, index) ->dict[T, U]: return {self.key_at(index): self.value_at(index)}
    
    def key_at(self, index) ->T:
        try: return self._manipulator.key_order[index]
        except IndexError as ie: raise IndexError(f"{type(self).__name__} index out of range") from None
       

class CanonicalDict(md):
    """CanonicalDict is an dict variant which has canonical values.
       it takes a function 'checker(existing_value, new_value)' and uses it upon adding every new key-value pairs.
       if it(checker) returns Ture → considers 'equal' and sets existing_value to the new key turning it into an alias of that value.
       if however returns False with every existing values. it'll considered an 'unique' value and it would set the key-value normally
    """
    
    def __init__(self, func: Callable[[Any, Any], bool], /, *args, **kwargs): super().__init__(CanonicalM(func), *args, **kwargs)
    @property
    def checker(self): return self._manipulator.checker


class TypedDict(md):
    """Typed containers enforces value type within specific types."""
    
    def __init__(self, allowed_keys: tuple[type], allowed_values: tuple[type], /, *args, **kwargs): super().__init__(TypedM(ts(allowed_keys), ts(allowed_values) ), *args, **kwargs)
    @property
    def allowed_types(self) ->dict[str, tuple[type] ]: return mpt({"key": self._manipulator.allowed_keys,"value": self._manipulator.allowed_values})


class QuantumDict(md):
    def __init__(self, *args, **kwargs): super().__init__(QuantumM(), *args, **kwargs)
   
    def entangle(self, a: Hashable, b: Hashable) ->None: self._manipulator.entangle(a, b)


class DualValueDict(md):
    def __init__(self, *args, **kwargs): super().__init__(DualValueM(), *args, **kwargs)
    @property
    def extra_values(self): return self._manipulator.extra_vals
    
    
class FixSizedDict(md):
    def __init__(self, *args, **kwargs): super().__init__(FixSizedM(), *args, **kwargs)
   
   
class LifetimeDict(lt, md): pass
    

class SizedDict(st, md): pass
     
    
class MemorySizedDict(mst, md): pass


if __name__=="__main__":
    pr=FixSizedDict({8:9,0:55,776:8})
    rp=DualValueDict(gg=False, huh=set(), gt=True)
    rp.extra_values["gg"]=100
    print(rp, rp.extra_values)
    pr[22]=9
    print(pr)

