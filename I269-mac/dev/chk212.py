import sympy as sp
rho, c, W = sp.symbols("rho c W")
K = -2*c/sp.pi
A = 1 + c*(rho**2+1) + K*(rho + (rho**2+1)*sp.atan(rho))
R = sp.sqrt(1+rho**2)
P = 2/rho - sp.diff(A,rho)/A
Q = 1/R**4 - sp.diff(A,rho)/(A*rho*R**2) - 2/(A*R**2) + W**2/A**2
def L(Y): return sp.diff(Y,rho,2) - P*sp.diff(Y,rho) - Q*Y
for cv in (-1, sp.Rational(-3,10)):
    print("W=0, Y=R:", sp.N(L(R).subs({c:cv, W:0, rho:1}), 20))
    # Y = R times const ; try Y = R + k*something?  test the candidate static: Y = R*(1 - ???)
