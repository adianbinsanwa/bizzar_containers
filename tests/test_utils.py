from src import *
import pytest as ptst


tl=TypedContainers[list](int)
ts=TypedContainers[set](int)
td=TypedContainers[dict](int, str)

print(tl, ts, td, sep="\n\n", end="\n\n")
 
@ptst.mark.parametrize("v", [8, 22, 89, 9])
def test_list(v):
    tl.append(v); assert tl[-1]==v

@ptst.mark.parametrize("v", [8, 22, 89, 9])
def test_set(v):
    ts.add(v); assert v in ts

@ptst.mark.parametrize("k,v", [(8,"8"), (99,"99"), (45,"54"), (100, "80")])
def test_dict(k,v):
    td[k]=v; assert td[k]==v

###########################################################################

@ptst.mark.parametrize("v", [("8", 2.56, bool(), [77,45])])
def test_list_at_init(v):
    tl.__class__(v)

@ptst.mark.parametrize("v", [("8", 2.56, bool(), [77,45])])
def test_list_at_init(v):
    ts.__class__(v)

@ptst.mark.parametrize("v", [(("8", 8), (2.56, "8"), (5, bool() ), (True, [77,45]) )])
def error_dict_at_init(v):
    td.__class__(v)


##########-errors-##########

@ptst.mark.parametrize("v", [False, {}, "88", set()])
def error_list(v):
    with ptst.raises(TypeError): tl.append(v)

@ptst.mark.parametrize("v", [False, {}, "88", set()])
def error_set(v):
    with ptst.raises(TypeError): ts.add(v)

@ptst.mark.parametrize("k,v", [([], False), ("6", {}), (9.36,"88"), (dict(),set() )])
def error_dict(k, v):
    with ptst.raises(TypeError): td[k]=v

###########################################################

@ptst.mark.parametrize("v", [("8", 2.56, bool(), [77,45])])
def error_list_at_init(v):
    with ptst.raises(TypeError): tl.__class__(v)

@ptst.mark.parametrize("v", [("8", 2.56, bool(), (77, 99) )])
def error_set_at_init(v):
    with ptst.raises(TypeError): ts.__class__(v)

@ptst.mark.parametrize("v", [(("8", 8), (2.56, "8"), (5, bool() ), (True, [77,45]) )])
def error_dict_at_init(v):
    with ptst.raises(TypeError): td.__class__(v)


sl=SizedContainers[list](10)
ss=SizedContainers[set](10)
sd=SizedContainers[dict](10)

print(sl, ss, sd, sep="\n\n", end="\n\n")



msl=MemorySizedContainers[list](1000)
mss=MemorySizedContainers[set](1000)
msd=MemorySizedContainers[dict](1000)

print(msl, mss, msd, sep="\n\n", end="\n\n")


hdl= HideSeekList()
ras= RadioActiveSet()
ll= LifetimeList(10)
ld= LifetimeDict(10)

print(hdl, ras, ll, ld, sep="\n\n", end="\n\n")


fsd= FixSizedDict()
cd= CanonicalDict(lambda x,y: isinstance(x, type(y) ) )
dvd= DualValueDict()
id_= IndexedDict()

print(fsd, cd, dvd, id_, sep="\n\n")


