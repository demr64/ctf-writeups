from sage.all import *
from random import randint

a = 288260533169915
p = 1007621497415251
'''
FLAG = b'crypto{????????????????????}'

def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)
        if b == '1':
            ciphertext.append(n)
        else:
            n = -n % p
            ciphertext.append(n)
    return ciphertext


print(encrypt_flag(FLAG))
'''
pt = b"crypto{"
t = ''.join([bin(i)[2:].zfill(8) for i in pt])
F = GF(p)
p = F(p)
a = F(a)

with open("values.txt", "r") as f:
    arr = f.read().strip().split(",")
    arr = [F(x) for x in arr]
print(len(t))
l = -1
byte = ''
strpt = "crypto{"
for i in range(55, len(arr)):
    if i >= len(t):
        l+=1
        if l == 8:
            strpt += chr(int((byte), 2))
            print(strpt)
            byte = ''
            l = 0
        try:
            x = discrete_log(arr[i], a)
            byte += '1'
            continue
        except:
            try:
                byte += '0'
                x = -arr[i]
                x= discrete_log(x, a)
            except:
                  continue
        continue
    if t[i] == '1':
        try:
            x = discrete_log(arr[i], a)
            byte += '1'
            print(x)
        except:
              continue
    else:
        try:
            byte += '0'
            x = -arr[i]
            x= discrete_log(x, a)
            print(x)
        except:
              continue





