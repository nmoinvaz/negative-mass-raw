import sys, time
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import remainder as rm
rm.CACHE = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache"
names = sys.argv[1].split(",")
items = dict(rm.data_items())
for n in names:
    for h in rm.HL:
        t = time.time()
        rm.run_data(items[n], h, n)
        print(n, h, f"{time.time()-t:.0f}s", flush=True)
