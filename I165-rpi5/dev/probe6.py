import pickle, sympy as sp
U_,B_,V_,S_=sp.symbols('u b v s')
NC = pickle.load(open("NC4new.pkl","rb"))[0]
fl1,_ = pickle.load(open("g1_fl.pkl","rb")); fl2,_ = pickle.load(open("g2_fl.pkl","rb"))
f1 = [f for f,m in fl1[1] if len(sp.Poly(f,U_,B_,V_,S_).terms())>1][0]
f2 = fl2[1][0][0]
def sg(e): return str(sp.expand(e)).replace("**","^")
open("p6_in.sing","w").write(f"""ring r=32003,(u,b,v,s),dp;
option(redSB);
short=0;
poly f0={sg(NC)};
poly f1={sg(f1)};
poly f2={sg(f2)};
ideal I=f0,f1,f2;
int t0=rtimer;
ideal G=std(I);
"std time",rtimer-t0,"size",size(G),"dim",dim(G),"mult",mult(G);
"degrees of lead:",deg(G[1]);
quit;
""")
