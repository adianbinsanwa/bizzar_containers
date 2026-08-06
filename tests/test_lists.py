from src import list_types as lt
#from pytest import raises, fixture, mark

test=[8,9,0,2,3,0,5,6]


def lifetime():
    d=lt['Lifetime'](5, test)
    for i in range(5): iter(d)
    assert all(i not in d for i in test), f"Lifetime issue {d}"

def lifespan():
    d=lt['Lifetime'](5, [0,9,0])
    for i in range(5): d[0]
    assert d.check_lifespan(0)==2, f"lifespan not decreasing {d.check_lifespan(0)=}"

lifetime()
lifespan()
