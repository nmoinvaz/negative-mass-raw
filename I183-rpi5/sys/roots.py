import json, subprocess, sys
import numpy as np
B='/home/nathan/Source/negative-mass-i183/notes/warp/conical_global/target/release/conical_global'
fi, c, L = sys.argv[1], sys.argv[2], sys.argv[3]
out = subprocess.run([B,'series',fi,c,L],capture_output=True,text=True).stdout
ser = json.loads(out)[0]
st = ser['state']
print('start n_rel', ser['n_rel'])
def pstr(x): return f"{x[0]!r}:{x[1]!r}"
def coefs(F,F1,e):
    a3 = 2*F*e**2*(F**2-e**2-1)
    a2 = F1*e*(4*F**3+F**2*F1*e**3+6*F**2*F1*e-6*F*e**2-4*F-F1*e**5-3*F1*e**3-2*F1*e)
    a1 = 2*F1**2*(F**3+F**2*F1*e**3+6*F**2*F1*e+2*F*F1**2*e**4+4*F*F1**2*e**2-3*F*e**2-F-F1*e**5-3*F1*e**3-2*F1*e)
    a0 = F1**3*(F**2*F1*e**2+2*F**2*F1+4*F*F1**2*e**3+8*F*F1**2*e-2*F*e+F1**3*e**6+4*F1**3*e**4+4*F1**3*e**2-F1*e**4-3*F1*e**2-2*F1)
    return [a3,a2,a1,a0]
for x1 in [float(a) for a in sys.argv[4:]]:
    o = subprocess.run([B,'walkstate',str(float(L)),pstr(st[0]),pstr(st[1]),pstr(st[2]),str(x1),fi],capture_output=True,text=True).stdout
    r = json.loads(o.splitlines()[-1])
    s = r['state']; F,F1,F2 = s[0][0],s[1][0],s[2][0]
    co = coefs(F,F1,x1)
    rts = np.roots(co)
    # finite-root estimate and -F1/eta
    print(f"eta={x1:g} out={r['outcome']} x={r['x']:g} F={F:.6e} F1={F1:.4e} F2={F2:.4e} -F1/eta={-F1/x1:.4e} roots={[complex(z) for z in rts]}")
