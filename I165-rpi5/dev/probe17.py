import pickle, sys, sympy as sp
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
p = int(sys.argv[1]); s_start=int(sys.argv[2]); s_cnt=int(sys.argv[3]); out=sys.argv[4]
def sg(e): return str(e).replace("**","^")
def poly_txt(d):
    return "+".join(f"({sp.Rational(c).p}{'/'+str(sp.Rational(c).q) if sp.Rational(c).q!=1 else ''})*u^{a}*b^{bb}*v^{c2}*s^{dd}" for (a,bb,c2,dd),c in d.items())
txt = f"ring r={p},(t,u,b,v,s),dp;\noption(redSB);\nshort=0;\n"
for nm in ["f0","f1","f2","f11"]: txt += f"poly {nm}={poly_txt(G[nm])};\n"
txt += f"poly Dl={sg(Dl)};\n"
txt += f"""
int k; string fn="{out}";
for(k={s_start};k<{s_start+s_cnt};k++){{
  poly g0=subst(f0,s,k); poly g1=subst(f1,s,k); poly g2=subst(f2,s,k); poly g11=subst(f11,s,k);
  poly P=u*subst(Dl,s,k);
  ideal J=g0,g1,g2,g11,1-t*P;
  matrix T; ideal Gb=liftstd(J,T);
  write(":a "+fn, "S "+string(k)+" G1 "+string(Gb[1])+" n "+string(size(Gb)));
  int i; for(i=1;i<=ncols(J);i++){{ write(":a "+fn, "C "+string(i)+" "+string(T[i,1])); }}
  kill g0,g1,g2,g11,P,J,T,Gb,i;
}}
quit;
"""
open(f"p17_{s_start}.sing","w").write(txt)
