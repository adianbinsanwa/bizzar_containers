from __future__ import annotations
from types import MappingProxyType as mpt
from .BaseModels import (

ManipulatorList, ManipulatorSet, ManipulatorDict,
ManipulatorTuple, ManipulatorFrozenSet, ManipulatorFrozenDict,
ManipulatorProtocol)


from .BaseSequence import (

TypedList, SizedList, MemorySizedList,
RadioActiveList, LifetimeList, HideSeekList,
GroupTuple)


from .BaseSet import (

TypedSet, SizedSet, GroupSet, MemorySizedSet,
IndexedSet, RadioActiveSet, LifetimeSet,
UnaryGraphSet, BinaryGraphSet, TrinaryGraphSet,
IndexedFrozenSet, GroupFrozenSet)


from .BaseMapping import (

TypedDict, SizedDict, GroupDict, MemorySizedDict,
RadioActiveDict, LifetimeDict, IndexedDict,
CanonicalDict, FixSizedDict, DualValueDict, 
UnaryGraphDict, BinaryGraphDict, TrinaryGraphDict,
IndexedFrozenDict, GroupFrozenDict)

#family hierarchy
#will recive their own *name*Comtainers:
    #main:- family whom implements in all 3 types and their immutable counterparts
    #majot:- family whom implements only in the 3 types
#else:
    #minor:- family whom implements 2/3 types
    #sub:- family whom is implements 1 type


#families as as invariants
ManipulatorContainers=mpt({list: ManipulatorList, dict: ManipulatorDict, set: ManipulatorSet,
                           tuple: ManipulatorTuple, mpt: ManipulatorFrozenDict, frozenset: ManipulatorFrozenSet})


GroupContiners=mpt({tuple: GroupTuple, set: GroupSet, frozenset: GroupFrozenSet, 
                    dict: GroupDict, mpt: GroupFrozenDict})

TypedContainers=mpt({list: TypedList, dict: TypedDict, set: TypedSet})

SizedContainers=mpt({list: SizedList, dict: SizedDict, set: SizedSet})

MemorySizedContainers=mpt({list: MemorySizedList, dict: MemorySizedDict, set: MemorySizedSet})

RadioActiveContainers=mpt({list: RadioActiveList, dict: RadioActiveDict, set: RadioActiveSet})

LifetimeContainers=mpt({list: LifetimeList, dict: LifetimeDict, set: LifetimeSet})


#families as types
sequence_types=mpt({
'mutable': mpt({'Manipulator': ManipulatorList, 'Sized': SizedList, 'Typed': TypedList, 'MemorySized': MemorySizedList,
           'RadioActive': RadioActiveList, 'Lifetime': LifetimeList, 'HideSeek': HideSeekList,
           }),      
           
'Immutable': mpt({"Manipulator": ManipulatorTuple, "Group": GroupTuple,
           }),         
})


set_types=mpt({
'mutable': mpt({'Manipulator': ManipulatorSet, 'Sized': SizedSet, 'Typed': TypedSet, 'MemorySized': MemorySizedSet,
            'RadioActive': RadioActiveSet, 'Lifetime': LifetimeSet, 'Indexed': IndexedSet,
            
            'Graph': mpt({'Unary': UnaryGraphSet, 'Binary': BinaryGraphSet, 'Trinary': TrinaryGraphSet}),
           }),     
           
'Immutable': mpt({"Manipulator": ManipulatorFrozenSet, "Indexed": IndexedFrozenSet, "Group": GroupFrozenSet,
           }),
})


mapping_types=mpt({
'mutable': mpt({'Manipulator': ManipulatorDict, 'Sized': SizedDict, 'Typed': TypedDict, 'MemorySized': MemorySizedDict,
            'RadioActive': RadioActiveDict,'Lifetime': LifetimeDict, 'Indexed': IndexedDict, 'Canonical': CanonicalDict,
            'DualValue': DualValueDict, 'FixSized': FixSizedDict,
            
            'Graph': mpt({'Unary': UnaryGraphDict, 'Binary': BinaryGraphDict, 'Trinary': TrinaryGraphDict}),
           }),
           
'Immutable': mpt({"Manipulator": ManipulatorFrozenDict, "Indexed": IndexedFrozenDict, "Group": GroupFrozenDict,
           }),
})



def convert(container, family: mpt[type, type], *args, **kwargs): return family[type(container)](container, *args, **kwargs)




__all__=[#types
         "sequence_types",
         "set_types",
         "mapping_types",
         
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
         
         #tuples
         "ManipulatorTuple",
         "GroupTuple",
         
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
         
         #frozensets
         "ManipulatorFrozenSet",
         "IndexedFrozenSet",
         "GroupFrozenSet",
         
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
         
         #frozendicts
         "ManipulatorFrozenDict",
         "IndexedFrozenDict",
         "GroupFrozenDict",
         
         #others
         "ManipulatorProtocol",
         "convert",
         ]
         
__version__="1.4.1"