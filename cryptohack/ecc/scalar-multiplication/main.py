from sage.all import *

#E:Y2=X3+497X+1768mod9739
def double_and_add(E, P, n):
    Q = P
    R = E(0)
    while n > 0:
        if n % 2 == 1:
            R += Q
        Q += Q
        n = n//2
    return R
F = GF(9739)
coeffs = [0, 0, 0, 497, 1768]
E = EllipticCurve(F, coeffs)
X=E(5323,5438)
P=E(2339,2213)
print(double_and_add(E, P, 7863))
