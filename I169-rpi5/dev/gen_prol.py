import sys
def gen(p,q,sat="al0",case="d",char=32003,fname="prol.sing",extra=""):
    """Singular script: prolongation ideal of D=0 in the (n; alpha,beta,gamma,delta) formulation."""
    al=[f"al{k}" for k in range(p+1)]; be=[f"be{k}" for k in range(p+1)]
    ga=[f"ga{k}" for k in range(q+1)]; de=[f"de{k}" for k in range(q+1)]
    vars_=["n0","n1","n2","n3","io","v"]+al+be+ga+de+["t"]
    s=f"ring r={char},({','.join(vars_)}),dp;\n"
    # derivations
    dx_terms = ["diff(f,n0)*n1","diff(f,n1)*(al0*n0+be0*n1)","diff(f,n2)*n3","diff(f,n3)*(al0*n2+be0*n3)"]
    for k in range(p):
        dx_terms.append(f"diff(f,al{k})*al{k+1}"); dx_terms.append(f"diff(f,be{k})*be{k+1}")
    dr_terms = ["diff(f,n0)*n2","diff(f,n1)*n3","diff(f,n2)*(de0*n0+ga0*n2)","diff(f,n3)*(de0*n1+ga0*n3)","diff(f,io)*(-io^2)"]
    for k in range(q):
        dr_terms.append(f"diff(f,ga{k})*ga{k+1}"); dr_terms.append(f"diff(f,de{k})*de{k+1}")
    s+="proc dx(poly f){ return("+"+".join(dx_terms)+"); }\n"
    s+="proc dr(poly f){ return("+"+".join(dr_terms)+"); }\n"
    s+="""
poly u = n0+v;
poly pi_ = al0*n0+be0*n1;
poly lam = (ga0+io)*n2+de0*n0;
poly P = -(n1^2+u*pi_);
poly Q2 = -lam;
poly Z2 = n3;
poly Y2 = 2*n1*n2+u*n3;
poly h2 = n2^2;
poly D = h2^3-4*h2*P^2-h2*Q2^2+h2*Y2^2+h2*Z2^2-2*P*(Y2^2-Z2^2)+2*Q2*Y2*Z2;
"""
    s+="ideal I;\npoly cur=D; poly row;\nint i,j;\n"
    s+=f"for(i=0;i<={p};i++){{ row=cur; for(j=0;j<={q};j++){{ I=I,row; row=dr(row); }} cur=dx(cur); }}\n"
    satpoly = {"al0":"al0","de0":"de0","none":"1"}[sat]
    s+=f"poly Wn=n0*n3-n1*n2;\n"
    extra_gens=""
    if case=="b":   # alpha == 0 identically
        extra_gens=",".join(f"al{k}" for k in range(p+1))
    if case=="c":
        extra_gens=",".join(f"de{k}" for k in range(q+1))
    if extra_gens: s+=f"I=I,{extra_gens};\n"
    s+=f"I=I,t*Wn*{satpoly}-1;\n"
    s+="option(redSB); option(prot);\nideal G=std(I);\nprint(\"size\"); print(size(G)); print(\"G1\"); print(G[1]); print(\"dim\"); print(dim(G));\nquit;\n"
    open(fname,"w").write(s)
if __name__=="__main__":
    p,q=int(sys.argv[1]),int(sys.argv[2]); sat=sys.argv[3]; case=sys.argv[4]
    gen(p,q,sat,case,fname=sys.argv[5])
