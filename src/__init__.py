from __future__ import annotations
from types import MappingProxyType as mpt
from .BaseModels import ManipulatorList, ManipulatorSet, ManipulatorDict, BaseManiuatorProtocol
from .BaseSequence import TypedList, SizedList, MemorySizedList, LifetimeList, HideSeekList
from .BaseSet import TypedSet, SizedSet, MemorySizedSet, RadioActiveSet
from .BaseMapping import TypedDict, SizedDict, MemorySizedDict, LifetimeDict, IndexedDict, CanonicalDict, QuantumDict 

ManipulatorContainers=mpt({list: ManipulatorList, dict: ManipulatorDict, set: ManipulatorSet})
TypedContainers=mpt({list: TypedList, dict: TypedDict, set: TypedSet})
SizedContainers=mpt({list: SizedList, dict: SizedDict, set: SizedSet})
MemorySizedContainers=mpt({list: MemorySizedList, dict: MemorySizedDict, set: MemorySizedSet})


def convert(container, family: mpt[type, type], *args, **kwargs): return family[type(container)](container, *args, **kwargs)


__all__=[#families
         "ManipulatorContainers",
         "SizedContainers",
         "TypedContainers",
         "MemorySizedContainers",
         
         #lists
         "ManipulatorList",
         "SizedList",
         "TypedList",
         "MemorySizedList",
         "LifetimeList",
         "HideSeekList",
         
         #sets
         "ManipulatorSet",
         "SizedSet", 
         "TypedSet",
         "MemorySizedSet",
         "RadioActiveSet",
         
         #dicts
         "ManipulatorDict",
         "SizedDict",
         "TypedDict",
         "MemorySizedDict",
         "LifetimeDict",
         "IndexedDict",
         "CanonicalDict",
         "QuantumDict", 
         
         #others
         "BaseManiuatorProtocol",
         ]