import sys, pickle
sys.path.insert(0,'/home/nathan/Source/negative-mass-i264/notes/wormhole_largeD')
import mpmath as mp
import identity_review as ir
mp.mp.dps=100
Om=ir.shifted_omegas({})
out={}
for tag in ('roots_b440_N160_n40_w0.5','roots_b500_N190_n44_w0.4'):
    nodes,end=pickle.load(open('%s/cache_rec/%s.pkl'%(sys.argv[1],tag),'rb'))
    acc,ab=ir.accumulate(nodes,Om)
    out[tag]=(end['l'],[acc['Gdef%d'%k] for k in range(2,8)])
    print(tag,'l_end',mp.nstr(end['l'],6),' '.join(mp.nstr(acc['Gdef%d'%k],4) for k in range(2,8)))
(l1,g1),(l2,g2)=out.values()
print('ratio G(cutoff2)/G(cutoff1):',' '.join(mp.nstr(b/a,4) for a,b in zip(g1,g2)))
print('exp((l1-l2)/2) =',mp.nstr(mp.exp((l1-l2)/2),4))
