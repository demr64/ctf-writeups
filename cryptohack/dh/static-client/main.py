from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
from pwn import *
import json

'''
Alice and Bob have share their values, B, g, p, A and the ct, iv.
|🗲 insight:
When talking to Bob we notice that if we send g = A, A = 1 then
Bob will compute it's private key as 1^b = 1 mod p, but when talking to us:
A^b = secret mod p
which is the secret we needed to decrypt their old messages.
'''

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):

    # Derive AES key from shared secret
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
    io = remote("socket.cryptohack.org", 13373)

    d = json.JSONDecoder()
    #ALIce
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    p = i['p']
    g = i['g']
    A = i['A']
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    B = i['B']
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    iv = i['iv']
    ct = i['encrypted']
    s = {'p':p, 'g':A, 'A':hex(1)}
    io.sendline(json.dumps(s).encode())
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    Ab = i['B']
    print(decrypt_flag(bytes_to_long(bytes.fromhex(Ab[2:])), iv, ct))
solve()

