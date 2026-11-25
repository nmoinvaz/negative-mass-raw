import sympy as sp
G,r,W=sp.symbols("G r W",real=True)
for cs in (1,-1):
  for ep in (1,-1):
    c=sp.Integer(cs)
    W2=G**2+2*c**2
    # H = W*B_k with sign s=+1 (k), -1 (m): B = G^2+4c^2 + s*(5 c eps W - 2cG/(rho W))*... for k: +5c eps W - 2cG r/W
    for s,name in ((1,"k"),(-1,"m")):
        H=(G**2+4*c**2)*W + s*(5*c*ep*W2 - 2*c*G*r)
        Gp=ep*W2-G*r
        Wp_over=G*Gp/W   # W' = G G'/W
        Hp=sp.diff(H,G)*Gp+sp.diff(H,W)*Wp_over+sp.diff(H,r)*(-r**2)
        # solve r from H=0
        rs=sp.solve(H,r)[0]
        Hp_r=sp.together(Hp.subs(r,rs))
        num=sp.numer(Hp_r)
        num=sp.expand(num)
        # reduce W powers using W^2=W2
        num=sp.Poly(num,W)
        p0=0;p1=0
        for (e,),co in num.terms():
            if e%2==0: p0+=co*W2**(e//2)
            else: p1+=co*W2**(e//2)
        p0=sp.expand(p0);p1=sp.expand(p1)
        # p0 + p1 W = 0 -> p0^2 - p1^2 W2 = 0
        N=sp.factor(sp.expand(p0**2-p1**2*W2))
        # real roots with G != 0
        rts=[sp.N(q,8) for q in sp.Poly(N,G).nroots() if abs(sp.im(q))<1e-12] if N.has(G) else []
        print("c",cs,"eps",ep,name,"N=",N)
        # which real roots G satisfy p0+p1*W=0 with W=+sqrt, and r>0
        sel=[]
        for q in rts:
            qv=sp.re(q); Wv=sp.sqrt(qv**2+2)
            val=(p0+p1*W).subs({G:qv,W:Wv})
            rv=rs.subs({G:qv,W:Wv})
            sel.append((float(qv),float(val),float(rv)))
        print("   real roots (G, p0+p1W, r):",sel)
