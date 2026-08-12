vals = "2f26 3026 \
     202f 1c06 4207 5c10 5413 5a15 3a05 571c\
     3b0d 471b 543a 0a53 1d45 1874 8091 47b6\
     7271 76b3 9aa8 fd9a e7aa 89e3 fb82 df5a  \
     6d57 9d35 fd25 816e 0000 0000 4945 4e44 \
     ae42 6082" 
tigr = "".join(vals.split())
xor = b"codetiger"
tigr = bytes.fromhex(tigr)
print("".join([chr(xor[i % len(xor)] ^ tigr[i]) for i in range(0, len(tigr))]))

