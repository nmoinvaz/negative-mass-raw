"""Singular prolongation ideal for case (c): u = A(x) R(rho) + B(x). Unknown jets A_k, B_k, R_k, io = 1/rho."""
import sys
def gen(p,q,fname,sat="W3R1",char=32003):
    A=[f"A{k}" for k in range(p+3)]; B=[f"B{k}" for k in range(p+3)]; R=[f"R{k}" for k in range(q+3)]
    vs=A+B+R+["io","t"]
    s=f"ring r={char},({','.join(vs)}),dp;\n"
    dxt=[f"diff(f,A{k})*A{k+1}" for k in range(p+2)]+[f"diff(f,B{k})*B{k+1}" for k in range(p+2)]
    drt=[f"diff(f,R{k})*R{k+1}" for k in range(q+2)]+["diff(f,io)*(-io^2)"]
    s+="proc dx(poly f){ return("+"+".join(dxt)+"); }\nproc dr(poly f){ return("+"+".join(drt)+"); }\n"
    s+="""poly u=A0*R0+B0;
poly ux=A1*R0+B1; poly uxx=A2*R0+B2; poly ur=A0*R1; poly uxr=A1*R1; poly lap=A0*(R2+io*R1);
poly P=-(ux^2+u*uxx); poly Q2=-lap; poly Z2=uxr; poly Y2=2*ux*ur+u*uxr; poly h2=ur^2;
poly D=h2^3-4*h2*P^2-h2*Q2^2+h2*Y2^2+h2*Z2^2-2*P*(Y2^2-Z2^2)+2*Q2*Y2*Z2;
"""
    s+="ideal I; poly cur=D; poly row; int i,j;\n"
    s+=f"for(i=0;i<={p};i++){{ row=cur; for(j=0;j<={q};j++){{ I=I,row; row=dr(row); }} cur=dx(cur); }}\n"
    s+="poly W3=A1*B2-A2*B1;\n"
    s+=f"I=I,t*W3*R1-1;\n"
    s+="ideal G=std(I);\nprint(size(G)); print(G[1]); print(dim(G));\nquit;\n"
    open(fname,"w").write(s)
p,q=int(sys.argv[1]),int(sys.argv[2]); gen(p,q,sys.argv[3])
