from typing import Any, TypeVar, Iterator, Hashable, Optional, Callable
from dataclasses import dataclass as dtc, field
from .BaseModels import ManipulatorDict as md

missing=object()
T=TypeVar("T")



@dtc(slots=True)
class IndexedM:
    key_order: list[Hashable]=field(init=False, default=None)
    
    def create(self, obj): self.key_order=[i for i in obj]
        
    def set(self, obj, base_action: Callable[[], None], value: Any, key: Hashable|object=missing):
        if (target:= value if key is missing else key) not in self.key_order: self.key_order.append(target)
        base_action()
   
    def delete(self, obj, base_action: Callable[[], None], key: Hashable):
        if key in self.key_order: self.key_order.pop(self.key_order.index(key) )
        base_action()
     

##########-invariant types-##########    


class IndexedType:
    """IndexedType tracks items's insertion order. and you can access them via their index"""
    
    def __init__(self, *args, **kwargs): super().__init__(IndexedM(), *args, **kwargs)
        
        
 
    