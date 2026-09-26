#!/usr/bin/env sage -python
from sage.all import *
from random import SystemRandom, randrange, randint
import fpylll.fplll.lll as lll
from fpylll import IntegerMatrix
import time


def gen_keypair(n):
    # Generating Private Key:
    # Generating random superincreasing set b
    b = []
    s = pow(2, n - 1)
    for i in range(0, n):
        value = SystemRandom().randrange(max(s + 1, pow(2, n + i - 1)), pow(2, n + i))
        b.append(value)
        s += value
    # Generating M such that M > sum
    M = SystemRandom().randrange(max(s + 1, pow(2, 2 * n - 1)), pow(2, n * 2))
    # Generating W such that W and M are coprime
    while True:
        W = SystemRandom().randrange(2, M)
        if gcd(W, M) == 1:
            break
    private_key = (b, M, W)
    # Calculating Public Key:
    public_key = [(x * W) % M for x in b]
    return (public_key, private_key)


def verify_privatekey(private_key):
    if gcd(private_key[1], private_key[2]) != 1:
        print("\nError: M and W are not coprime!\n")
        return False
    sum_ = 0
    for i in range(0, len(private_key[0])):
        if private_key[0][i] <= sum_:
            print(i)
            print(private_key[0][i], sum_)
            print("\nError: b is not a superincreasing sequence!\n")
            return False
        sum_ += private_key[0][i]
    if sum_ >= private_key[1]:
        print("\nError: M is not greater than the sum of all elements of b!\n")
        return False
    return True


def info(key, val):
    print(key + "\n" + str(val))
    print(
        "------------------------------------------------------------------------------------------------"
    )


def generate_lattice(a, l):
    A = []
    for i in range(l - 1):
        A.append([])
        for j in range(l - 1):
            if i == j:
                A[i].append(-a[0])
            else:
                A[i].append(0)
    A.append([])
    for j in range(l - 1):
        A[l - 1].append(a[j + 1])
    return A


def main():
    l = 10
    n = 72
    success_num = 0
    perfect_num = 0
    total = 1000
    print("## n=%d, l=%d, total=%d ##\n"%(n,l,total))
    pubkey = [int(line) for line in open("pubkey.txt").readlines()[0:72]]
    ciphertexts = [int(line) for line in open("ciphertext.txt").readlines()[1:]]
    start_time=time.time()
    a = pubkey
    t = generate_lattice(a, l)
    A = IntegerMatrix(l, l - 1)
    A.set_matrix(t)
    V = IntegerMatrix(l, l)

    reduced_basis = lll.lll_reduction(A, U=V)

    vector_s = reduced_basis[1]

    flag = vector_s[8] < 0  

    K = []
    if flag:
        for i in range(l):
            K.append(-V[1][i - 1])
    else:
        for i in range(l):
            K.append(V[1][i - 1])

    M1 = a[0]
    U1 = K[0]
    b1 = []
    for i in range(n):
        b1.append((a[i] * U1) % M1)
    for c in ciphertexts:
        plaintext = []
        c1 = (c * U1) % M1
        for i in range(len(b1) - 1, -1, -1):
            if c1 >= b1[i]:
                plaintext.append(1)
                c1 -= b1[i]
            else:
                plaintext.append(0)
            if c1 == 0:
                break
        for j in range(i):
            plaintext.append(0)
        plaintext.reverse()
        result = b''
        result += int("".join(map(str, plaintext)), 2).to_bytes(9, "big")
        print(result.decode(), end="")
if __name__ == "__main__":
    main()
