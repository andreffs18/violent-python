#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import optparse
from scapy.all import *
from scapy.error import Scapy_Exception


def find_google(packet):
    if not packet.haslayer(Raw):
        return

    payload = packet.getlayer(Raw).load
    if 'google' not in payload:
        return

    r = re.findall(r'(?i)\&q=(.*?)\&', payload)
    if r:
        search = r[0].split('&')[0]
        search = search.replace('q=', '').replace('+', ' ').replace('%20', ' ')
        print('[+] Searched For: {}'.format(search))


if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()

    if not options.interface:
        print(parser.usage)
        exit(0)

    interfaces = [options.interface]
    if options.interface == "all":
        interfaces = ["lo0", "gif0*", "stf0*", "en0", "en1",  "en2", "fw0",  "p2p0", "bridg",  "utun0"]

    for interface in interfaces:
        conf.iface = interface
        try:
            print('[*] Starting Google Sniffer using "{}" interface.'.format(interface))
            sniff(prn=find_google, timeout=60)
        except KeyboardInterrupt:
            continue
        except Scapy_Exception, e:
            print('[!] Error: {}'.format(e))





