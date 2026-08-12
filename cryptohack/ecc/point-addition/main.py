from sage.all import *
'''
let q and p
l = yq - yp // xq - xp -> is the angular coefficient;
xr = l^2 - xp - xq
yr = l(xp - xr) - yp

**derivation:
l is the coefficient. now we would want
y = lx + q and evaluate it in the sum of the two points. therefore:
y - yp = l(x - xp) -> y = lx - lxp + yp.

yr = lxr - lxp + yp
yr = l(xr - xp) + yp
which can be negated, and should, because we are getting the sum and then the negative, so
yr = l(xp - xr) - yp

🗲 insight:
now, substituting into the elliptic curve:
(we don't care about negating, since y is squared)
(l(x-xp) + yp)^2 = x^3 + ax + b
(l^2(x^2 - 2x(xp) + ...
so x^2 coeff is l^2.
this has three roots.
xp, xq and xr.
(x-xp))(x-xq)(x-xr)
by vieta's formulas:
-> x^3 - (xr + xp + xq)x^2 + ...
but we know that l is this.
Therefore:
    l^2 =(xr + xp + xq),
    xr = l^2 - xp - xq
'''
def point_addition(E, P, Q):
    if P == E(0):
        return Q
    elif Q == E(0):
        return P
    elif Q[0] == P[0] and P[1] == -Q[1]:
        return E(0)
    if P != Q:
        l = (Q[1]-P[1])/(Q[0]-P[0])
    elif P == Q:
        l = (3*P[0]*P[0] + E.a4())/(2*P[1])
    xr = l*l - P[0] - Q[0]
    return E(xr, l*(P[0]-xr) - P[1])

#E:Y2=X3+497X+1768mod9739
N = 9739
F = GF(N)
coeffs = [0, 0, 0, 497, 1768]
E = EllipticCurve(F, coeffs)
#we can still use point addition in sagemath X+Y
P=E(493,5564)
Q=E(1539,4742)
R=E(4403,5202)
print(point_addition(E, P, point_addition(E, P, 
        point_addition(E, Q, R))))
