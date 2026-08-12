from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
from pwn import *
import json
'''
in an additive group we have a*g mod p insteaad of g^a mod p.
**insight:
we just find the inverse of g mod p, we compute it, and we have the private exponent
we can compute the key by computing then a*B and decrypt the flag
'''
io = remote("socket.cryptohack.org", 13380)
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
    #A
    line = io.recvuntil(b"Bob:").decode()
    decoder = json.JSONDecoder()
    intercepted, end = decoder.raw_decode(line[(line.find("{")):])
    p = bytes.fromhex(intercepted['p'][2:])
    A = bytes_to_long(bytes.fromhex(intercepted['A'][2:]))
    print(intercepted)
    #B
    line = io.recvuntil(b"Alice:").decode()
    intercepted, end = decoder.raw_decode(line[line.find("{"):])
    B = bytes_to_long(bytes.fromhex(intercepted['B'][2:]))
    print(intercepted)


    line = io.recvuntil(b"}").decode()
    intercepted, end = decoder.raw_decode(line[(line.find("{")):])
    print(intercepted)

    pw = pow(2, -1, bytes_to_long(p))
    a = pow(pw*A, 1, bytes_to_long(p))
    iv = intercepted['iv']
    encrypted_flag =intercepted['encrypted']
    shared_secret = pow(a*B, 1, bytes_to_long(p))
    print(decrypt_flag(shared_secret, iv, encrypted_flag))

solve()

