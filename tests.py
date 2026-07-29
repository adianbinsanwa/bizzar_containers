from src import *
import operator as op


tl=TypedContainers[list](int)
ts=TypedContainers[set](int)
td=TypedContainers[dict](int, str)

print(tl, ts, td, sep="\n\n", end="\n\n")

def type_stream():
    

def check_type_enforcement(f):
    assert f() "error"

check_type_enforcement(lambda: tl.append())

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


