docs={
'unary':"""UnaryGraphType is the first version of Graph type. it enforces one way connection between items like: parent --> child.
a sub-child= child's child, a super-parent= parent's parent

a child/sub-child cannot take it's parent/super-patent as it's own child.
when a item dies/gets removed, all of it childs and sub-childs would die regardless of the fact that they have other parents""",
        
'binary':"""BinaryGraphType is the sequal of UnaryGraphType. it enforces tow way connection between items like:- item <-> item
everything else is same as UnaryGraphType""",
         
'trinary':"""TrinaryGraphType is the sequal of BinaryGraphType. it enforces a fake three way connection between items like:-  neibours of 1:-(3,5,7,9), neibours of 0:-(2,4,6,8,10), new_link(0, 1)=(0,1,2,3,4,5,6,7,8,9,10).
 each new link makes so that if a is reachable from c via b, then a must be reachable from c directly too.
 essentially it performs cluster linking""",
          
'indexed':"""IndexedType tracks items's insertion order. and you can access them via their index""",

'group':"""<empty for further notice>""",

'sized':"""Sized containers takes and enforces a size range. the container would never exceed this range.""",

'typed':"""Typed containers enforces value type within specific types.""",

'memorysized':"""MemorySized containers is a variant of Sized containes. it counts capacity in memory bytes""",

'lifetime':"""LifetimeType containers's elements slowly decays after each access/iteration.""",

'radioactive':"""RadioActiveType enforces random decay. on each iteration there's a chance for an element to get removed(sometimes nothing happens too)""",

'manipulator': """BaseContainer/ManipulatorType is the base type for manipulator container family.
the manipulator given by the user controls the behavior when interacting with the container""",

'protocol': """BaseManipulatorProtocol is a blueprint for manipulator protocols
       there are six protocols:-
           create:- after instansiating the container "create" is called,
           iterate:- when iter() is called on the container "iterate" is called
           get:- when element accessing happens "get" is called
           set:- when setting a value happens "set" is called
           insert:- when expanding the container "insert" is called. it's an optional protocol. if not set it'll fallback to "set"
           delete:- when deleting an element "delete" is called
       note:- if the manipulator doesn't implement the target protocol. it'll switch to a base_protocol instead.
            otherwise the manipulator is expected to handle the action.""",
            
}

