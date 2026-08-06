from __future__ import annotations
from types import MappingProxyType as mpt
from .BaseModels import (

ManipulatorList, ManipulatorSet, ManipulatorDict,
ManipulatorProtocol)


from .BaseSequence import (

TypedList, SizedList, MemorySizedList,
RadioActiveList, LifetimeList, HideSeekList)


from .BaseSet import (

TypedSet, SizedSet, MemorySizedSet,
IndexedSet, RadioActiveSet, LifetimeSet,
UnaryGraphSet, BinaryGraphSet, TrinaryGraphSet)


from .BaseMapping import (

TypedDict, SizedDict, MemorySizedDict,
RadioActiveDict, LifetimeDict, IndexedDict,
CanonicalDict, FixSizedDict, DualValueDict,
UnaryGraphDict, BinaryGraphDict, TrinaryGraphDict)



#families as as invariants
ManipulatorContainers=mpt({list: ManipulatorList, dict: ManipulatorDict, set: ManipulatorSet})

TypedContainers=mpt({list: TypedList, dict: TypedDict, set: TypedSet})

SizedContainers=mpt({list: SizedList, dict: SizedDict, set: SizedSet})

MemorySizedContainers=mpt({list: MemorySizedList, dict: MemorySizedDict, set: MemorySizedSet})

RadioActiveContainers=mpt({list: RadioActiveList, dict: RadioActiveDict, set: RadioActiveSet})

LifetimeContainers=mpt({list: LifetimeList, dict: LifetimeDict, set: LifetimeSet})





#families as types
list_types=mpt({
'Manipulator': ManipulatorList, 'Sized': SizedList, 'Typed': TypedList, 'MemorySized': MemorySizedList,
'RadioActive': RadioActiveList, 'Lifetime': LifetimeList, 'HideSeek': HideSeekList
})


set_types=mpt({
'Manipulator': ManipulatorSet, 'Sized': SizedSet, 'Typed': TypedSet, 'MemorySized': MemorySizedSet,
'RadioActive': RadioActiveSet, 'Lifetime': LifetimeSet, 'Indexed': IndexedSet,
'Graph': mpt({'Unary': UnaryGraphSet, 'Binary': BinaryGraphSet, 'Trinary': TrinaryGraphSet})
})


dict_types=mpt({
'Manipulator': ManipulatorDict, 'Sized': SizedDict, 'Typed': TypedDict, 'MemorySized': MemorySizedDict,
'Lifetime': LifetimeDict, 'Indexed': IndexedDict, 'Canonical': CanonicalDict, 'DualValue': DualValueDict, 
'FixSized': FixSizedDict, 'Graph': mpt({'Unary': UnaryGraphDict, 'Binary': BinaryGraphDict, 'Trinary': TrinaryGraphDict})
})



def convert(container, family: mpt[type, type], *args, **kwargs): return family[type(container)](container, *args, **kwargs)




__all__=[#types
         "list_types",
         "set_types",
         "dict_types",
         
         #families
         "ManipulatorContainers",
         "SizedContainers",
         "TypedContainers",
         "MemorySizedContainers",
         "RadioActiveContainers",
         "LifetimeContainers",
         
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
         "UnaryGraphSet",
         "BinaryGraphSet",
         "TrinaryGraphSet",
         
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
         "UnaryGraphDict",
         "BinaryGraphDict",
         "TrinaryGraphDict",
         
         #others
         "ManipulatorProtocol",
         "convert",
         ]