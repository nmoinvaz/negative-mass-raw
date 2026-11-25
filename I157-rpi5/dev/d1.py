import sys, time, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
t0 = time.time()
import three_scalars as t3
print("import", time.time()-t0, flush=True)
Rs = t3.wall_frame(None)
print("wall_frame", time.time()-t0, flush=True)
R3 = Rs[:3,:3]
for i in range(3):
    for j in range(i,3):
        print(i,j,len(sp.Add.make_args(R3[i,j])) if (sp:=t3.sp) else 0)
h = t3.orbit_metric(R3, t3.WJ[0])
print("h", time.time()-t0, [len(t3.sp.Add.make_args(h[i,j])) for i in range(3) for j in range(i,3)], flush=True)
print(h)
pickle.dump((str(R3), str(h)), open(sys.argv[1]+"/R3h.pkl","wb"))
