import sys, math, time, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import throat_locus as tl
D = int(sys.argv[1]); hk = int(sys.argv[2]); out = sys.argv[3]
tl.job_stall(D, hk, out)
