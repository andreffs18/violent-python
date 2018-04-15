#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygeoip
import optparse

from utils import print_ip_details


if __name__ == '__main__':
    parser = optparse.OptionParser("usage %prog --ip <IP Address> [-d <database file>] ")
    parser.add_option('--ip', dest='ip', type='string', help='specify ip address')
    parser.add_option('-d', dest='database', type='string', default="GeoLiteCity.dat", help='specify database location address [default: %default]')

    (options, args) = parser.parse_args()

    if not options.ip:
        print(parser.usage)
        exit(0)

    client = pygeoip.GeoIP(os.path.join(os.getcwd(), options.database))
    print_ip_details(client, options.ip)