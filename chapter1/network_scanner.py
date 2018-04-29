#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import optparse


def get_banner(ip, port, timeout):
    """
    Open socket connection to given ip:port and 
    read first 1024 bytes from open socket connection
    """
    socket.setdefaulttimeout(timeout)
    s = socket.socket()
    try:
        s.connect((ip, port))
        ans = s.recv(1024)
        return ans
    except Exception, e:
        print("[-] Error {}:{} = {}".format(ip, port, e))
        return None
    
def check_vulnerabilities(banner, filename):
    """
    From given banner, check if from "filename" theres is any match
    """
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip('\n') in banner:
                print "[+] Server is vulnerable: {}".format(banner.strip('\n'))


if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog -n <network> -t <type of probe>')
    parser.add_option('-n', dest='network', type='string', default="192.168.1.X", help='specify network to search on (default: "192.168.0.X"')
    parser.add_option('--start_subnet', dest='start_subnet', type='int', default=1, help='specify which subnet should the scan start (default: "1"')
    parser.add_option('--end_subnet', dest='end_subnet', type='int', default=254, help='specify which subnet should the scan stop (default: "254"')
    # test telnet, ssh, smtp, http, imap and https ports
    parser.add_option('-p', dest='ports', type='string', default="21, 22, 25, 80, 110, 443", help='specify list of ports, separed by comma (default: "21, 22, 25, 80, 110, 443"')
    parser.add_option('--vul_filename', dest='vulnerabilities_filename', type='string', default="banners.txt", help='default file with list of vulnerabilities to compare (default: "banners.txt"')
    parser.add_option('--socket_timeout', dest='socket_timeout', type='int', default=2, help='default socket connection timeout (default: "2" seconds')
    (options, args) = parser.parse_args()

    # generate list of all possible ip's on subnet 192.168.1.0/24
    subnet = options.network.lower()
    subnet_string = subnet.replace("x", "{}")
    ip_list = map(lambda ip: subnet_string.format(ip), range(options.start_subnet, options.end_subnet))
    # test ports telnet, ssh, smtp, http, imap and https
    port_list = map(int, filter(None, map(lambda p: p.strip(), options.ports.split(","))))

    print("[*] Testing subnet of {} for {} ports: {}".format(subnet_string, len(port_list), options.ports))
    for ip in ip_list:
        for port in port_list:
            banner = get_banner(ip, port, timeout=options.socket_timeout)
            if banner:
                print("[+] Checking {}:{}".format(ip, port))
                check_vulnerabilities(banner, filename=options.vul_filename)

