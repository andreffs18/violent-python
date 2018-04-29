#!/usr/bin/python
# -*- coding: utf-8 -*-
import zipfile
import optparse
from tqdm import tqdm
from threading import Thread


def extract_file(zfile, password):
    """
    Try to extract files from secured zip file. Print password if that works
    """
    try:
        zfile.extractall(pwd=password)
        print("[+] Found password \"{}\"".format(password))
    except:
        pass
    

if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog --zipfile <secure zipfile> --test_passwords <file list of possible passwords>')
    parser.add_option('--zipfile', dest='zipfile', type='string', default="evil.zip", help='specify zip filename to crack (default: "evil.zip"')
    parser.add_option('--test_passwords', dest='test_passwords', type='string', default="dictionary.txt", help='specify file that contains list of possible passwords (default: "dictionary.txt"')
    (options, args) = parser.parse_args()
    
    zfile = zipfile.ZipFile(options.zipfile)
    with open(options.test_passwords) as dictionary_file:
        for possible_password in tqdm(dictionary_file.readlines()):
            password = possible_password.strip()
            t = Thread(target=extract_file, args=(zfile, password))
            t.start()