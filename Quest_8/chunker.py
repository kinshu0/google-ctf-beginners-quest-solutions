from base64 import b64decode
import chunk


with open('hideandseek.png', 'rb') as f:
    img_data = f.read()

class Chunk:
    def __init__(self, img_bytes):
        """
        img_bytes: bytearray
        """
        self.img_bytes = img_bytes
        self.chunks = [
            {
                'raw': img_bytes[:8],
                'type': 'file signature'
            },
        ]
        i = 8
        while i < len(img_bytes):
            length = int.from_bytes(img_bytes[i:i+4], 'big')
            raw = img_bytes[i: i+length+4]
            type = img_bytes[i+4:i+8]
            data = img_bytes[i+8: i+8+length]
            crc = img_bytes[i+8+length: i+8+length+4]
            chunk = {
                'length': length,
                'raw': raw,
                'type': type,
                'data': data,
                'crc': crc,
            }
            self.chunks.append(chunk)
            i += length+12


p = Chunk(img_data)

unique_chunks = set()

# for idx ,i in enumerate(p.chunks):
#     unique_chunks.add(i['type'])

# print(unique_chunks)
eDIH_data_sequential = [x['data'].decode() for x in p.chunks if x['type'] == b'eDIH']

print(''.join(eDIH_data_sequential))
print(b64decode(''.join(eDIH_data_sequential)))

# for idx ,i in enumerate(p.chunks):
#     print(i)
