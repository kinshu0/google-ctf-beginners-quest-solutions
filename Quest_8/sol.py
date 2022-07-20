

# with open('hideandseek.png', 'rb') as f:
#     a = f.read()

# a = bytearray(a)

# b = [chr(x) for x in a if x <= 126 and x >= 32]



# with open('dump.txt', 'w') as f:
#     f.write(''.join(b))
# print(b)

with open('dump.txt', 'r') as f:
    a = list(f.read())

i = 0

COMMA = '`'
ZERO = '0'
prev_comma = False
prev_zero = False
l = 0
start = -1

while i < len(a):

    curr = a[i]
    

    if (not prev_comma) and (not prev_zero) and curr != COMMA and curr != ZERO:
        pass

    elif (not prev_comma) and (not prev_zero) and curr == COMMA:
        start = i
        l += 1
        prev_comma = True

    elif (not prev_comma) and (not prev_zero) and curr == ZERO:
        start = i
        l += 1
        prev_zero = True    

    elif prev_comma and curr == ZERO:
        l += 1
        prev_zero = True
        prev_comma = False

    elif prev_zero and curr == COMMA:
        l += 1
        prev_comma = True
        prev_zero = False

    elif prev_comma and curr == COMMA and l > 1:
        a[start:start+l] = '\n'
        start += 1
        l = 1
        i = start + 1
        continue

    elif prev_zero and curr == ZERO and l > 1:
        a[start:start+l] = '\n'
        start += 1
        l = 1
        i = start + 1
        continue

    elif l > 1:
        a[start:start+l] = '\n'
        start = -1
        prev_comma = False
        prev_zero = False
        l = 0
        i = start + 1
        continue
        

    i+=1

with open('dump_proc2.txt', 'w') as f:
    f.write(''.join(a))
