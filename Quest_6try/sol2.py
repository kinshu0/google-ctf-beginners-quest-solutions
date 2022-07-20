with open('chall.txt', 'rb') as f:
    chall = f.read()

l = [x for x in chall.decode()]

l2 = [x.encode() for x in l]

l3 = []

l4 = b''

for c in l2:
    acc = 0
    if len(c) == 3:
        acc |= (c[2] & 0x3f)
        acc |= (c[1] & 0x3f) << 6
        acc |= (c[0] & 0xf) << 12
    else:
        raise Exception('bruh')
    l3.extend([(acc & 0xff00) >> 8, (acc & 0x00ff)])
    # l3.append(acc)
    # l4 += bin(acc)

print(l3[:10])

with open('maybesolution', 'wb') as f:
    f.write(bytes(l3))

