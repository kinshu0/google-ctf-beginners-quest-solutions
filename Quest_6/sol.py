with open('chall.txt', 'rb') as f:
    raw_contents = f.read()

# decoded_values = raw_contents.decode()

# vals_map = {}

# for i in decoded_values:
#     if i in vals_map:
#         vals_map[i] += 1
#     else:
#         vals_map[i] = 1

# # print(decoded_values[:10])
# print(vals_map)

# values = [ord(x) for x in raw_contents.decode()]


# content_bytes = []

# for x in values:
#     content_bytes.extend(list(x.to_bytes(-1*(-x.bit_length() // 8), 'big')))

# a = values[0].to_bytes(-1*(-values[0].bit_length() // 8), 'big')
# print(list(a))

# b = values[1].to_bytes(-1*(-values[1].bit_length() // 8), 'big')
# print(list(b))

# print(a, b)
# print([a, b])

# print([len(x) for x in content_bytes[:10]])
# print(content_bytes[:10])
# print([x for x in bytearray(content_bytes[:10])])
# print(bytes(content_bytes))

# with open('out.txt', 'wb') as f:
#     f.write(bytes(content_bytes))


# print(values[0].to_bytes())

# values = [x.to_bytes(-1*(-x.bit_length() // 8), 'big') for x in values]




# print(content_bytes[:10])

# with open('out.txt', 'wb') as f:
#     f.write(bytes(values))

# print(min(values), max(values))
# print(max(values) - min(values))
