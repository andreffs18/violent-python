#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import optparse
from scapy.all import *


def sniff_dot_11(p):
    if not p.haslayer(Dot11ProbeResp):
        return

    netName = p.getlayer(Dot11ProbeResp).info
    addr2 = p.getlayer(Dot11).addr2
    print('[+] Decloaked Hidden SSID :{} for MAC:{}'.format(netName, addr2))

    if not p.haslayer(Dot11Beacon):
        return

    if p.getlayer(Dot11Beacon).info != '':
        return

    addr2 = p.getlayer(Dot11).addr2
    print('[-] Detected Hidden SSID: with MAC:{}'.format(addr2))


def sniff_probe(p):
    if not p.haslayer(Dot11ProbeReq):
        return
    netName = p.getlayer(Dot11ProbeReq).info
    print('[+] Detected New Probe Request: {}'.format(netName))


if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog -i <interface> -t <type of probe>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    parser.add_option('-t', dest='type', type='string', help='specify 802.11 network ("beacon" or "probe")')
    (options, args) = parser.parse_args()

    if not options.interface and not options.type:
        print(parser.usage)
        exit(0)

    if options.type == "beacon":
        print_func = sniff_dot_11
    elif options.type == "probe":
        print_func = sniff_probe
    else:
        print("Invalid 802.11 type. Only \"probe\" or \"beacon\"")
        exit(0)

    try:
        print('[*] Starting Network 802.11 "{}" Sniffer...'.format(options.type.upper()))
        sniff(iface=options.interface, prn=print_func)
    except KeyboardInterrupt:
        exit(0)
