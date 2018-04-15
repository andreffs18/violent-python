#!/usr/bin/python
# -*- coding: utf-8 -*-
import dpkt
import socket
import optparse

from utils import print_ip_details


def print_pcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            print_ip_details(ip=src)
            dst = socket.inet_ntoa(ip.dst)
            print_ip_details(ip=dst)
            print('[+] Src: {} --> Dst: {}'.format(src, dst))
        except Exception as e:
            print('[!] Failed to print because: {}'.format(e))


if __name__ == '__main__':
    parser = optparse.OptionParser("usage %prog -f <filename>")
    parser.add_option('-f', dest='filename', type='string', help='specify .pcap filename')

    (options, args) = parser.parse_args()

    if not options.filename:
        print(parser.usage)
        exit(0)

    # read given pcap file
    pcap = dpkt.pcap.Reader(open(options.filename))
    print_pcap(pcap)
