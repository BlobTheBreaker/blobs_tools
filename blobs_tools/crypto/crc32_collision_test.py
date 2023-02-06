from zlib import crc32
from sys import exit

HASH_LEN = 8

hash_chars = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

for a in hash_chars:
    print(a)
    for b in hash_chars:
        print(a+b)
        for c in hash_chars:
            print(a+b+c)
            for d in hash_chars:
                for e in hash_chars:
                    for f in hash_chars:
                        for g in hash_chars:
                            for h in hash_chars:
                                hash_guess = a + b + c + d + e + f + g + h

                                message = '<script nonce="' + hash_guess + '">alert("test");</script>'

                                if hex(crc32(bytes(message, 'UTF-8'))).split('x')[1] == hash_guess:
                                    print(f'Collision found: {message} with {hash_guess}')
                                    exit()

