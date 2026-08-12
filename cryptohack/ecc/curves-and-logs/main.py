from sage.all import *
import hashlib

#E:Y2=X3+497X+1768mod9739,
F = GF(9739)
coeffs = [0,0,0,497,1768]
E = EllipticCurve(F, coeffs)
Qa=E(815,3190)
n = 1829
m = hashlib.sha1()
P = n*Qa
print(P[0])
m.update(str(P[0]).encode())
print(m.hexdigest())
