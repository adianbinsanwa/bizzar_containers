from __future__ import annotations
from typing import Any, Hashable, Callable;   from functools import partial as prtl
from dataclasses import dataclass, field;   from types import MappingProxyType as mpt
from .BaseModels import Typed_simplifier as ts, ManipulatorDict as md, SizedType as st, MemorySizedType as mst, RadioActiveType as rat, LifetimeType as lt
from .SubModels import IndexedType as it, UnaryGraphType as ugt, BinaryGraphType as bgt, TrinaryGraphType as tgt

dtc=prtl(dataclass, slots=True, eq=False)

##########-Manipulators-##########

@dtc
class DualValueM:
    extra_vals: dict[Any, Any]=field(init=False, default=None)
        
    def create(self, obj): self.extra_vals={i:None for i in obj}
        
    def set(self, obj, base_action: Callable[[], None], value, key: Hashable): base_action(); self.extra_vals.setdefault(key, None)
        
    def delete(self, obj, base_action: Callable[[], None], key: Hashable): self.extra_vals.pop(key); return base_action()
    

@dtc
class FixSizedM:
    size: int=field(init=False, default=None)
    
    def create(self, obj): self.size=len(obj)
    
    def set(self, obj, base_action, value, key: Hashable):
        if key in obj: base_action()
        else: raise SizedTypeError(f"cannot modify a {type(obj).__name__}'s size")
    
    def delete(self, obj, base_action, key): raise SizedTypeError(f"cannot modify a {type(obj).__name__}'s size")


@dtc
class CanonicalM:
    checker: Callable[[Any, Any], bool]
    
    def create(self, obj):
        d=obj._values.copy(); obj._values.clear()
        for k,v in d.items(): obj[k]=v
    
    def set(self, obj, base_action: Callable[[], None], value, key: Hashable):
        for k,v in obj.items():
            if self.checker(value, v): obj._values[key]=v; break
        else: base_action()


@dtc(frozen=True)
class TypedM:
    allowed_keys: tuple[type]
    allowed_values: tuple[type]
    
    def create(self, obj):
        for k,v in obj.items(): self.set(None, lambda: None, v, k)
    
    def set(self, obj, base_action: Callable[[], None], value, key: Hashable):
        if type(key) not in self.allowed_keys: raise TypeError(f"invalid key type, expected:-{' or '.join(f'{i.__name__}' for i in self.allowed_keys)}, got:-'{type(key).__name__}'")
        elif type(value) not in self.allowed_values: raise TypeError(f"invalid value type, expected:-{' or '.join(f'{i.__name__}' for i in self.allowed_values)}, got:-'{type(value).__name__}'")
        base_action()


##########-dict families-##########


class IndexedDict[T, U](it, md[T, U]):
    """IndexedDict allowes key, value, item access using index"""
    
    @property
    def indexes(self) ->tuple[T]: return tuple(self._manipulator.key_order)
     
    def value_at(self, index: int) ->U: return self[self.key_at(index)]
    
    def item_at(self, index: int) ->dict[T, U]: return {self.key_at(index): self.value_at(index)}
    
    def key_at(self, index: int) ->T:
        try: return self._manipulator.key_order[index]
        except IndexError as ie: raise IndexError(f"{type(self).__name__} index out of range") from None
            
            
class UnaryGraphDict(ugt, md):
    def _set(self, vals):
        for k,v in vals.items(): self[k]=v
    
    def _del(self, val): del self[val]
        
    def setdefault(self, key, default, /, *, links: dict[Hashable, Iterable[Hashable] ]={}): val=super().setdefault(key, default); self.new_link(links); return val
                    
            
class DualValueDict[T, U](md[T, U]):
    """DualValueDict is an inferior version of MultiValueDict. instead of multiple values it only provides one extra value slot
       meaning each key can have only two values. on normal access, set, delete you're only interacting with the mani value.
       if you want to set, get, delete an extra value then access d.extra_values. also when popping a key you'll get both values in a tuple
    """
    
    def __init__(self, *args, **kwargs): super().__init__(DualValueM(), *args, **kwargs)
    @property
    def extra_values(self) ->dict[T, Any]: return self._manipulator.extra_vals
    
    def pop(self, key: T, default: D=None) ->tuple[U|D, Any]: r=(self.get(key, default), self.extra_values.get(key, None) ); del self[key]; return r
       

class CanonicalDict(md):
    """CanonicalDict is an dict variant which has canonical values.
       it takes a function 'checker(existing_value, new_value)' and uses it upon adding every new key-value pairs.
       if it(checker) returns Ture → considers 'equal' and sets existing_value to the new key turning it into an alias of that value.
       if however returns False with every existing values. it'll considered an 'unique' value and it would set the key-value normally
    """
    
    def __init__(self, func: Callable[[Any, Any], bool], /, *args, **kwargs): super().__init__(CanonicalM(func), *args, **kwargs)
    @property
    def checker(self) ->Callable[[Any, Any], bool]: return self._manipulator.checker


class TypedDict(md):
    """Typed containers enforces value type within specific types."""
    
    def __init__(self, allowed_keys: tuple[type]|type, allowed_values: tuple[type]|type, /, *args, **kwargs): super().__init__(TypedM(ts(allowed_keys), ts(allowed_values) ), *args, **kwargs)
    @property
    def allowed_types(self) ->dict[str, tuple[type] ]: return mpt({"key": self._manipulator.allowed_keys,"value": self._manipulator.allowed_values})


class FixSizedDict(md):
    """FixSizedDict is a sub version of SizedDict. it enforces fix size while allowing mutation
   
    """
    
    def __init__(self, *args, **kwargs): super().__init__(FixSizedM(), *args, **kwargs)
   
    def swap(self, cur_key: Hashable, new_key: Hashable):
        if cur_key not in self: raise ValueError(f"invalid target key: {cur_key=} does not exist ")
        elif new_key in self: raise ValueError(f"key swapping collision: {new_key=} alread exists")
        val=self._values.pop(cur_key); self._values[new_key]=val
        
   
class LifetimeDict(lt, md):
    def setdefault(self, key: Hashable, default, lifespan: Optional[int]=None):
        if lifespan is None or key in self: return super().setdefault(key, default)
        self._values[key]=default; self._manipulator.items[key]=self._lifespan_is_valid(lifespan); return default


class BinaryGraphDict(bgt, UnaryGraphDict): pass


class TrinaryGraphDict(tgt, UnaryGraphDict): pass


class RadioActiveDict(rat, md): pass
    

class SizedDict(st, md): pass
     
    
class MemorySizedDict(mst, md): pass


if __name__=="__main__":
    pr=FixSizedDict({8:9,0:55,776:8})
    
    print(pr)

