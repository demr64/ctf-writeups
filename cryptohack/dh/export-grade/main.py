from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
from sage.all import *
from pwn import *
import json

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

def solve():
    io = remote("socket.cryptohack.org", 13379)

    line = io.recvuntil(b"}").decode()
    d = json.JSONDecoder()
    i, _ = d.raw_decode(line[line.find("{"):])
    i = {'supported':['DH64']}
    io.sendline(json.dumps(i).encode())
    line = io.recvuntil(b"}").decode()
    i, _ = d.raw_decode(line[line.find("{"):])
    print(i)
    io.sendline(json.dumps(i).encode())
    io.interactive()
#solve()
p = bytes_to_long(bytes.fromhex("de26ab651b92a129"))
F = GF(p)
g = F(bytes_to_long(bytes.fromhex("02")))
A = F(bytes_to_long(bytes.fromhex("1a7df3c9286109e1")))
B = F(bytes_to_long(bytes.fromhex("10d7483c94e6a699")))
iv = "348541d3ee8665c21d6146d1a8e87d87"
flag = "6de67e5537bce90c201a92adf1040f93abe585a92b75a971b57b795a90ba460c" 
key = pow(g, discrete_log(A, g)*discrete_log(B, g))
print(decrypt_flag(int(key), iv, flag))
