#!/usr/bin/python
# -*- coding: UTF-8 -*-

import base64
import os
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

def import_pk():
    with open('pub.pem', 'r') as f:
        key = RSA.importKey(f.read())
        return key

def get_hashes():
    hashes = {}
    os.system('ls -tr ./Moje\ dokumenty/*.txt >files.txt')
    with open('files.txt', 'r') as f:
        for i, name in enumerate(f.readlines(), 1):
            hashes[i] = name[17:-12]

    os.system('rm files.txt')
    return hashes

def get_encrypted_keys():
    keys_dir = './keys'
    keys = {}
    for i, name in enumerate(sorted(os.listdir(keys_dir)), 1):
        print(name)
        with open(keys_dir + '/' + name, 'r') as file:
            keys[i] = bytes_to_long(base64.b64decode(file.read()))

    return keys

def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

def modinv(a, m):
    g, x, _ = xgcd(a, m)
    if g == 1:
        return x % m

def franklin_reiter(n, c1, c2):
    num = c2 + 2 * c1 - 1
    denom = c2 - c1 + 2
    return (num * modinv(denom, n)) % n

def get_digests(rsa, keys):
    digests = {}
    key = franklin_reiter(rsa.n, keys[1], keys[2])
    offset = 0

    for i in range(1, 23):
        next_key = key + offset
        next_digest = SHA256.new(long_to_bytes(next_key)).digest()
        digests[i] = base64.b64encode(next_digest)
        offset += 1

    return digests

def get_args(hashes, digests):
    result = ''
    for i in range(1, 23):
        result += ' ' + str(hashes[i]) + ' ' + str(digests[i])
    return result

if __name__ == "__main__":
    hashes = get_hashes()
    rsa = import_pk()
    digests = get_digests(rsa, get_encrypted_keys())

    wannacry = 'python wannacry.py -d' + get_args(hashes, digests)
    print(wannacry + '\n')
    for i in range(1, 23):
        print(str(hashes[i]) + '    ' + str(digests[i]))
    print('\n')

    os.system(wannacry)
    #os.system('tail -c +17 ./Moje\ dokumenty/75943_articlefeature.jpg ' +
    #'>./Moje\ dokumenty/75943_articlefeature_fixed.jpg')
    #os.system('rm ./Moje\ dokumenty/75943_articlefeature.jpg')
    #os.system('rm -r ./Moje\ dokumenty/*.README.txt')
