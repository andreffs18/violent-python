import os
import pygeoip


def get_default_client(database="GeoLiteCity.dat"):
    return pygeoip.GeoIP(os.path.join(os.getcwd(), database))


def print_ip_details(client=None, ip=""):
    """From given "pygeoip" client and IP address, print details"""
    if not client:
        client = get_default_client()

    rec = client.record_by_name(ip)
    city = rec['city']
    region = rec.get('region_name', rec.get('region_code'))
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print('[*] Target: {} Geo-located. '.format(ip))
    print('[+] {}, {}, {}'.format(city, region, country))
    print('[+] Latitude: {}, Longitude: {}'.format(lat, long))

