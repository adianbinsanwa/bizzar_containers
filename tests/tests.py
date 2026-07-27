from src import *
import operator as op

tl=TypedContainers[list](allowed_types=int)
ts=TypedContainers[set](allowed_types=int)
td=TypedContainers[dict](allowed_keys=int, allowed_values=str)

print(tl, ts, td)


sl=SizedContainers[list](max_size=10)
ss=SizedContainers[set](max_size=10)
sd=SizedContainers[dict](max_size=10)

print(sl, ss, sd)



msl=MemorySizedContainers[list](max_size=1000)
mss=MemorySizedContainers[set](max_size=1000)
msd=MemorySizedContainers[dict](max_size=1000)

print(msl, mss, msd)



fsd= FixSizedDict({5:10,2:9})
cd= CanonicalDict(lambda x,y: isinstance(x, type(y) ) )
dvd= DualValueDict()
id_= IndexedDict()

print(fsd, cd, dvd, id_)


for i in (int(), str(), list(), set((8,6)), tuple(), bool(), dict(uhh=9) ):
        for j in (ts, ):
            try: print(op.sub(j, i) )
            except (TypeError, NotImplementedError) as e: print(e)
            try: print(op.sub(i,j) )
            except (TypeError, NotImplementedError) as e2: print(e2)
            try: print(op.isub(j,i) )
            except (TypeError, NotImplementedError) as e3: print(e3)
            print("-----------------------------")