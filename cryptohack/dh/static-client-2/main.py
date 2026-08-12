from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
import hashlib
from pwn import *
import json
from sage.all import *

'''
**insight
this is a small group confinement attack so we may just use pohlig hellman with another very smooth prime
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
    io = remote("socket.cryptohack.org", 13378)

    d = json.JSONDecoder()
    #ALIce
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    p = i['p']
    intp = bytes_to_long(bytes.fromhex(p[2:]))
    g = i['g']
    A = i['A']
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    B = i['B']
    intB = bytes_to_long(bytes.fromhex(B[2:]))

    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    iv = i['iv']
    flag = i['encrypted']
    print(i)
    fake = 74780951352567738838476507203405198502291020468903961016122955937936930303397056351356066320584550093532063720734114191579292432663668412364209738792084486694662127221352467512968642785275502014161326684993365993179874999143520288604119066614708346782458193276297353061079986185981636414551007141277290493746035023464491835024158471527094919603144242726157747682376730941361058786503236831187956531223094015787268326397222420316009142960518056827823806075414379601761263723454336658559
    F = GF(fake)
    dump = {'p':hex(fake), 'g':hex(2), 'A':A}
    io.sendline(json.dumps(dump).encode())
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    print(i)
    B = i['B']
    l = io.recvuntil(b"}").decode()
    i, end = d.raw_decode(l[(l.find("{")):])
    ds = discrete_log(F(int(B[2:], 16)), F(2))
    print(ds)
    print(decrypt_flag(pow(int(A[2:], 16), int(ds), intp), iv, flag))
solve()


