import pickle, sympy as sp, collections, sys
U_,B_,V_,S_=sp.symbols('u b v s')
NC = pickle.load(open("NC4new.pkl","rb"))[0]
fl1,_ = pickle.load(open("g1_fl.pkl","rb")); fl2,_ = pickle.load(open("g2_fl.pkl","rb"))
f1 = [f for f,m in fl1[1] if len(sp.Poly(f,U_,B_,V_,S_).terms())>1][0]
f2 = fl2[1][0][0]
for nm,f in (("f0",NC),("f1",f1),("f2",f2)):
    P = sp.Poly(f,U_,B_,V_,S_); ms = P.monoms()
    print(nm, "terms", len(ms), "total deg", P.total_degree(), "deg u,b,v,s", [max(m[i] for m in ms) for i in range(4)],
          "v parity", collections.Counter(m[2]%2 for m in ms))
def sg(e): return str(sp.expand(e)).replace("**","^")
s0 = int(sys.argv[1]) if len(sys.argv)>1 else 7
p = 32003
open(f"p7_s{s0}.sing","w").write(f"""ring r={p},(u,b,v),dp;
option(redSB);
short=0;
poly f0={sg(NC.subs(S_,s0))};
poly f1={sg(f1.subs(S_,s0))};
poly f2={sg(f2.subs(S_,s0))};
ideal I=f0,f1,f2;
int t0=rtimer;
ideal G=std(I);
"slice s={s0}: std time",rtimer-t0,"size",size(G),"dim",dim(G),"mult",mult(G);
"lead degrees:",deg(G[1]);
quit;
""")
