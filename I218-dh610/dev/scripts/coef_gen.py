import math
from math import sqrt

def m4_entries(rho, lam, L, As, A1):
    x0 = As*rho
    x1 = -x0
    x2 = rho**2
    x3 = A1*x2 + A1
    x4 = x2 + 1
    x5 = 1/x4
    x6 = 1/As
    x7 = x5*x6
    x8 = (1/2)*L
    x9 = x7*((1/2)*A1*x4 + x1)
    x10 = math.sqrt(2)
    x11 = x10*x5
    x12 = 2*As
    x13 = x10*x6
    x14 = 4*lam
    x15 = A1**2
    return (1.0*(-x7*(x1 + x3)), 1.0*(x7*(As*x8 + lam*x4)), 1.0*(x9), 1.0*(-x11), 1.0*(x6), 1.0*(-A1*x6), 1.0*(x6), 1.0*(0), 1.0*(rho*x5), 1.0*(x5*x8), 1.0*(x9), 1.0*(x11), 1.0*(-1/4*x13*(A1*rho + L - x12)), 1.0*(-1/8*x13*(A1*L + rho*x14)), 1.0*((1/8)*x10*(2*A1*x0 - 4*As + L*x12 + x14*x2 + x14 - x15*x2 - x15)/As**2), 1.0*((1/2)*x7*(-4*x0 + x3)))

def m3_entries(rho, lam, As, A1):
    x0 = As*rho
    x1 = rho**2
    x2 = A1*x1 + A1
    x3 = x1 + 1
    x4 = 1/x3
    x5 = 1/As
    x6 = x4*x5
    x7 = (1/2)*x6
    x8 = math.sqrt(2)*x4
    x9 = -x8
    x10 = -4*x0
    x11 = A1*rho
    x12 = 2*x1
    x13 = As**2
    x14 = (1/2)*lam
    x15 = rho**4
    return (1.0*(-x7*(-2*x0 + x2)), 1.0*(-x6*(-x0 + x2)), 1.0*(x9), 1.0*(0), 1.0*(x7*(x10 + x2)), 1.0*(x9), 1.0*(-1/4*x5*x8*(A1*rho**3 - As*x12 + x11 + x12 + 2)), 1.0*(-x8*(-1/8*A1**2*(x15 + 1) + lam*x1 + (1/4)*x11*(As*x1 + As - x11) - 1/2*x13 + x14*x15 + x14)/x13), 1.0*(x7*(A1*x3 + x10)))

def g3_entries(rho, lam, As, A1):
    x0 = math.sqrt(As)
    x1 = rho**2
    x2 = x1 + 1
    x3 = As*rho
    x4 = A1*x2
    x5 = 2*x1
    x6 = x0/x2**(3/2)
    return (1.0*((1/2)*(A1*(-2*x3 + x4) - 4*lam*x2)/(x0*math.sqrt(x2))), 1.0*(x6*(A1*rho**3 + A1*rho - As*x5 + x5 + 2)), 1.0*(-math.sqrt(2)*x6*(-x3 + (1/2)*x4)))

def m4_entries_c(rho, lam, L, As, A1):
    x0 = As*rho
    x1 = -x0
    x2 = rho**2
    x3 = A1*x2 + A1
    x4 = x2 + 1
    x5 = 1/x4
    x6 = 1/As
    x7 = x5*x6
    x8 = (1/2)*L
    x9 = x7*((1/2)*A1*x4 + x1)
    x10 = math.sqrt(2)
    x11 = x10*x5
    x12 = 2*As
    x13 = x10*x6
    x14 = 4*lam
    x15 = A1**2
    return ((-x7*(x1 + x3))+0j, (x7*(As*x8 + lam*x4))+0j, (x9)+0j, (-x11)+0j, (x6)+0j, (-A1*x6)+0j, (x6)+0j, (0)+0j, (rho*x5)+0j, (x5*x8)+0j, (x9)+0j, (x11)+0j, (-1/4*x13*(A1*rho + L - x12))+0j, (-1/8*x13*(A1*L + rho*x14))+0j, ((1/8)*x10*(2*A1*x0 - 4*As + L*x12 + x14*x2 + x14 - x15*x2 - x15)/As**2)+0j, ((1/2)*x7*(-4*x0 + x3))+0j)

def m3_entries_c(rho, lam, As, A1):
    x0 = As*rho
    x1 = rho**2
    x2 = A1*x1 + A1
    x3 = x1 + 1
    x4 = 1/x3
    x5 = 1/As
    x6 = x4*x5
    x7 = (1/2)*x6
    x8 = math.sqrt(2)*x4
    x9 = -x8
    x10 = -4*x0
    x11 = A1*rho
    x12 = 2*x1
    x13 = As**2
    x14 = (1/2)*lam
    x15 = rho**4
    return ((-x7*(-2*x0 + x2))+0j, (-x6*(-x0 + x2))+0j, (x9)+0j, (0)+0j, (x7*(x10 + x2))+0j, (x9)+0j, (-1/4*x5*x8*(A1*rho**3 - As*x12 + x11 + x12 + 2))+0j, (-x8*(-1/8*A1**2*(x15 + 1) + lam*x1 + (1/4)*x11*(As*x1 + As - x11) - 1/2*x13 + x14*x15 + x14)/x13)+0j, (x7*(A1*x3 + x10))+0j)

def g3_entries_c(rho, lam, As, A1):
    x0 = math.sqrt(As)
    x1 = rho**2
    x2 = x1 + 1
    x3 = As*rho
    x4 = A1*x2
    x5 = 2*x1
    x6 = x0/x2**(3/2)
    return (((1/2)*(A1*(-2*x3 + x4) - 4*lam*x2)/(x0*math.sqrt(x2)))+0j, (x6*(A1*rho**3 + A1*rho - As*x5 + x5 + 2))+0j, (-math.sqrt(2)*x6*(-x3 + (1/2)*x4))+0j)
