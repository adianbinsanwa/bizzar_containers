from __future__ import annotations
from types import MappingProxyType as mpt
from .BaseModels import ManipulatorList, ManipulatorSet, ManipulatorDict, ManiuatorProtocol
from .BaseSequence import TypedList, SizedList, MemorySizedList, RadioActiveList, HideSeekList
from .BaseSet import TypedSet, SizedSet, MemorySizedSet, IndexedSet, RadioActiveSet, LifetimeSet
from .BaseMapping import TypedDict, SizedDict, MemorySizedDict, RadioActiveDict, LifetimeDict, IndexedDict, CanonicalDict, FixSizedDict, DualValueDict

#families as as invariants
ManipulatorContainers=mpt({list: ManipulatorList, dict: ManipulatorDict, set: ManipulatorSet})
TypedContainers=mpt({list: TypedList, dict: TypedDict, set: TypedSet})
SizedContainers=mpt({list: SizedList, dict: SizedDict, set: SizedSet})
MemorySizedContainers=mpt({list: MemorySizedList, dict: MemorySizedDict, set: MemorySizedSet})
RadioActiveContainers=mpt({list: RadioActiveList, dict: RadioActiveDict, set: RadioActiveSet})

#families as types
list_types=mpt({
'Manipulator': ManipulatorList, 'Sized': SizedList, 'Typed': TypedList, 'MemorySized': MemorySizedList,
'RadioActive': RadioActiveList, 'HideSeek': HideSeekList
})

set_types=mpt({
'Manipulator': ManipulatorSet, 'Sized': SizedSet, 'Typed': TypedSet, 'MemorySized': MemorySizedSet,
'RadioActive': RadioActiveSet, 'Lifetime': LifetimeSet, 'Indexed': IndexedSet
})

dict_types=mpt({
'Manipulator': ManipulatorDict, 'Sized': SizedDict, 'Typed': TypedDict, 'MemorySized': MemorySizedDict,
'Lifetime': LifetimeDict, 'Indexed': IndexedDict, 'Canonical': CanonicalDict, 'DualValue': DualValueDict, 
'FixSized': FixSizedDict
})

def convert(container, family: mpt[type, type], *args, **kwargs): return family[type(container)](container, *args, **kwargs)


__all__=[#families
         "ManipulatorContainers",
         "SizedContainers",
         "TypedContainers",
         "MemorySizedContainers",
         "RadioActiveContainers",
         
         #lists
         "ManipulatorList",
         "SizedList",
         "TypedList",
         "MemorySizedList",
         "RadioActiveList",
         "HideSeekList",
         
         #sets
         "ManipulatorSet",
         "SizedSet", 
         "TypedSet",
         "MemorySizedSet",
         "RadioActiveSet",
         "LifetimeSet",
         "IndexedSet",
         
         #dicts
         "ManipulatorDict",
         "SizedDict",
         "TypedDict",
         "MemorySizedDict",
         "RadioActiveDict",
         "LifetimeDict",
         "IndexedDict",
         "CanonicalDict",
         "FixSizedDict",
         "DualValueDict",
         
         #others
         "ManiuatorProtocol",
         ]