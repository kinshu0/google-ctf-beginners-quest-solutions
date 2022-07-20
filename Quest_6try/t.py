from base64 import b16encode, b64decode, b64encode, b85decode


data = bytes('hello', encoding='utf-8')

# print(data)
# print([chr(x) for x in data])
# print([x for x in data])
# print(b16encode(data))
# print([x for x in b16encode(data)])
# print([chr(x) for x in b16encode(data)])
# print(b64encode(data))
# print([x for x in b64encode(data)])
# print([chr(x) for x in b64encode(data)])

# w_data = bytes(data, encoding='utf-8')

# with open('new.txt', 'wb') as f:
#     f.write()

"""
base16
6 0110
8 1000
6 0110
5 0101
6 0110
C 1100
6 0110
C 1100
6 0110
F 1111

0110100001100101011011000110110001101111

base64
a 26 011010
G 6 000110
V 21 010101
s 44 101100
b 27 011011
G 6 000110
8 60 111100
= padding
42 bits

011010000110010101101100011011000110111100

"""
import struct
def b85decode(b):
    """Decode the base85-encoded bytes-like object or ASCII string b

    The result is returned as a bytes object.
    """
    # Delay the initialization of tables to not waste memory
    # if the function is never called

    _b85alphabet = (b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    b"abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~")
    _b85dec = [None] * 256
    for i, c in enumerate(_b85alphabet):
        _b85dec[c] = i

    if isinstance(b, str):
        b = b.encode('ascii')
    
    padding = (-len(b)) % 5
    b = b + b'~' * padding
    out = []
    packI = struct.Struct('!I').pack
    for i in range(0, len(b), 5):
        chunk = b[i:i + 5]
        acc = 0
        
        for c in chunk:
            acc = acc * 85 + _b85dec[c]
        
        out.append(packI(acc))
        

    result = b''.join(out)
    if padding:
        result = result[:-padding]
    return result



def custom_encode(data, base):
    bits_per_block = 2**base
    pass




def custom_decode(data, base):
    pass

with open('test.txt', 'wb') as f:
    f.write(b85decode(data))

with open('test.txt', 'rb') as f:
    print(b64decode(f.read()))