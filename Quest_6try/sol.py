# """
# First tried uncompressing the file which failed
# """

# import zlib

# print(zlib.decompress(open('chall.txt', 'rb').read()))



"""
Compare header of chall to gzip headers
"""


"""
Try and find the base of the encoding by reading the smallest and largest value of a byte
"""

from base64 import b85decode


char_frequency = {}

with open('chall.txt', 'rb') as f:
    chall = f.read()

for i in chall:
    if i in char_frequency:
        char_frequency[i] += 1
    else:
        char_frequency[i] = 1

alphabet = [None]*512
for i, c in enumerate(range(min(char_frequency), max(char_frequency) + 1)):
    alphabet[c] = i
print(alphabet)

print(sorted(char_frequency))
print(len(char_frequency))
print(max(char_frequency) - min(char_frequency))


# print(b85decode(chall))
print([x for x in chall[:10]])
print([alphabet[x] for x in chall[:10]])
print([chr(alphabet[x]) for x in chall[:10]])
# print(b85decode(bytes([alphabet[x] for x in chall])))

# for i in chall:
#     if i > largest:
#         largest = i
#     if i < smallest:
#         smallest = i

# print('Smallest:', smallest, 'Largest:', largest)
# print(chall)

