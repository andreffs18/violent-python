#!/usr/bin/python
# -*- coding: utf-8 -*-
import crypt
import optparse
from tqdm import tqdm


def test_password(crypt_pass, dictionary_filename):
    """
    From given cryptografic password we can find a match on our "database" 
    """
    salt = crypt_pass[:2]
    with open(dictionary_filename, 'r') as dictionary:
        for word in tqdm(dictionary.readlines()):
            word = word.strip()
            crypt_test = crypt.crypt(word, salt)
            if crypt_pass == crypt_test:
                print("[+] Found password: \"{}\"".format(word))
                return word
        print("[-] Password not found.")
    return
    

if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog --unknown_passwords <file list of hashed passwords> --test_passwords <file list of possible passwords>')
    parser.add_option('--unknown_passwords', dest='unknown_passwords', type='string', default="passwords.txt", help='specify file that contains list of unknown hashed passwords (default: "passwords.txt"')
    
    parser.add_option('--test_passwords', dest='test_passwords', type='string', default="dictionary.txt", help='specify file that contains list of possible passwords (default: "dictionary.txt"')
    (options, args) = parser.parse_args()

    with open(options.unknown_passwords) as unknown_passwords:
        for line in unknown_passwords.readlines():
            if ":" in line:
                user = line.split(':')[0]
                crypt_pass = line.split(':')[1].strip(' ')
                print("[*] Cracking Password For: {}".format(user))
                test_password(crypt_pass, options.test_passwords)
