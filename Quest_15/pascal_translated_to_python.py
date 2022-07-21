def rol_left(x, n):
    return (x << n) & (2**64 - 1) | (x >> (64 - n))

check_key_pad_code = None

code = [int(x) for x in '3333319552798534']

x = 0
i = 0

for digit in code:
    if digit < 0 or digit > 9:
        check_key_pad_code = False
        exit()

    x = x | (digit << i)
    i += 4

x = x ^ (0o1275437152437512431354)
x = rol_left(x, 10)

a = x & 1229782938247303441
b = x & 0o0210421042104210421042
c = x & rol_left(1229782938247303441, 2)
d = x & rol_left(0o0210421042104210421042, 2)

if a == 0x0100101000011110 and b == 0x2002220020022220 and c == 0x4444040044044400 and d == 0x8880008080000880:
    check_key_pad_code = True
else:
    check_key_pad_code = False



print(check_key_pad_code)