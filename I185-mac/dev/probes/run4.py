import sys
exec(open("explore4.py").read().split("import sys\nfi, c")[0])
flow(1.5, 3000, 1e-4, 12, mp.mpf("0.01"))
