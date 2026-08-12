# 2^128 collision protection!
BLOCK_SIZE = 32

# Nothing up my sleeve numbers (ref: Dual_EC_DRBG P-256 coordinates)
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

# Lets work with bytes instead!
W_bytes = b''.join([x.to_bytes(4,'big') for x in W])
X_bytes = b''.join([x.to_bytes(4,'big') for x in X])
Y_bytes = b''.join([x.to_bytes(4,'big') for x in Y])
Z_bytes = b''.join([x.to_bytes(4,'big') for x in Z])

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len]*padding_len)

def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]

def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return  data[-x:] + data[:-x]

def scramble_block(block):
    for _ in range(40): 
        block = xor(W_bytes, block) #XOR block and bytes
        block = rotate_left(block, 6) #rotate by 6 40 times -> an actual rotation 
        #of 240 to the left,
        block = xor(X_bytes, block) #XOR block and bytes
        block = rotate_right(block, 17) #rotate by 40 times -> rotation of 17*40
        #rotation of 680 to the right, but the block is 32
        #therefore we are rotating by 24
    return block

def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes) #getting a state
    msg_padded = pad(msg) #we pad the message with the number of missing bytes
    msg_blocks = blocks(msg_padded) #we divide hte message in blocks of 32
    for i,b in enumerate(msg_blocks):
        mix_in = scramble_block(b) 
        for _ in range(i): #for block position
            #still, rotations and xor.
            mix_in = rotate_right(mix_in, i+11) #rotate 11 and 6 times i times so 
            #for block 0 -> 11, 6; 1 -> 12, 7; ...
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i+6)
        initial_state = xor(initial_state,mix_in)
    #so we have S(x) = R(x) ^ C -> T(s(x))
    #= 
    return initial_state.hex()


