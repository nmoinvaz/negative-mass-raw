exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i226/6ce098f9-1c29-4ea1-b637-485e454079a0/scratchpad/slab.py").read())
D, hn, Tc, X = 6, "0.00125", 8.0, 12.0
h, ps = pstar(D, hn); A = ps - 1e-8
base = go(D, h, "S", A, Tc, X, "base row")
go(D, h, "S", A, Tc, X, "diag f8 (control)", engine="diag")
go(D, h, "S", A, Tc, X, "RK4 sub=4", sub=4)
go(D, h, "S", A, Tc, X, "RK4 sub=16", sub=16)
go(D, h, "S", A, Tc, X, "ray_pert 1e-7 (mutation)", ray_pert=1e-7)
go(D, h, "S", A, Tc, X, "ray_pert 1e-9", ray_pert=1e-9)
go(D, h, "S", A, Tc, X, "spike (3000,1000,1e-10) mid", engine="diag", spike=(3000, 1000, 1e-10))
go(D, h, "S", A, Tc, X, "spike corner (2,2,1e-10)", engine="diag", spike=(2, 2, 1e-10))
go(D, h, "static", 0.0, 4.0, 6.0, "static dense data", dense=True)
go(D, h, "static", 0.0, 4.0, 6.0, "static RK4 data")
