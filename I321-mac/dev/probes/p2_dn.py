import sympy as sp, time, pickle
t0=time.time()
V,U,ang,ph,eta=sp.symbols('V U ang ph eta')
X=[V,U,ang,ph]
f=lambda n: sp.Function(n)(V,U)
r0,Om0,Th0=f('r0'),f('Om0'),f('Th0')
dr,dOm,dth,hv,hu=f('dr'),f('dOm'),f('dth'),f('hv'),f('hu')
P0,P1,P2=sp.symbols('P0 P1 P2')   # potential, d/dth, d^2/dth^2 at the background
r=r0+eta*dr; Om=Om0+eta*dOm; Th=Th0+eta*dth
g=sp.zeros(4,4)
g[0,0]=eta*hv; g[1,1]=eta*hu; g[0,1]=g[1,0]=-Om
g[2,2]=r**2; g[3,3]=r**2*sp.sin(ang)**2
gi=sp.zeros(4,4)
det2=g[0,0]*g[1,1]-g[0,1]**2
gi[0,0]=g[1,1]/det2; gi[1,1]=g[0,0]/det2; gi[0,1]=gi[1,0]=-g[0,1]/det2
gi[2,2]=1/g[2,2]; gi[3,3]=1/g[3,3]
n=4
Gam=[[[sum(gi[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d])) for d in range(n))/2 for c in range(n)] for b in range(n)] for a in range(n)]
def ric(b,d):
    s=sum(sp.diff(Gam[a][b][d],X[a])-sp.diff(Gam[a][b][a],X[d]) for a in range(n))
    s+=sum(Gam[a][a][k]*Gam[k][b][d]-Gam[a][d][k]*Gam[k][b][a] for a in range(n) for k in range(n))
    return s
print('start',time.time()-t0)
Vp=P0+eta*P1*dth      # potential on Th0+eta dth, first order
Vtp=P1+eta*P2*dth
dT=[sp.diff(Th,x) for x in X]
E={}
for nm,(i,j) in {'VV':(0,0),'VU':(0,1),'UU':(1,1),'thth':(2,2)}.items():
    E[nm]=ric(i,j)+2*dT[i]*dT[j]-Vp*g[i,j]
sq=sp.sqrt(-g.det()/sp.sin(ang)**2)*sp.sin(ang)   # sqrt(-det g)
box=sum(sp.diff(sq*gi[a,b]*dT[b],X[a]) for a in range(n) for b in range(n))/sq
E['sc']=-2*box-Vtp
print('Ricci built',time.time()-t0)
E0={k:e.subs(eta,0) for k,e in E.items()}
E1={k:sp.diff(e,eta).subs(eta,0) for k,e in E.items()}
print('linearized',time.time()-t0)
# thth: remove the angular dependence
E0['thth']=sp.simplify(E0['thth']); E1['thth']=sp.simplify(E1['thth'])
E0['sc']=sp.simplify(E0['sc']); E1['sc']=sp.simplify(E1['sc'])
for k in E0:
    print(k,'E0 ops',sp.count_ops(E0[k]),'E1 ops',sp.count_ops(E1[k]), E1[k].has(ang))
print(E0['VV']); print(E0['VU']); print(E0['thth']); print(E0['sc'])
pickle.dump((E0,E1),open('E01.pkl','wb'))
print('done',time.time()-t0)
