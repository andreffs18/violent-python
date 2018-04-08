#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename, dirname
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS


def find_images(url):
    """Return all img's on given url"""
    print('[+] Finding images on {}'.format(url))
    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, "html5lib")
        return soup.findAll('img')
    except Exception as e:
        print("[-] Failed to get images from {} because: {}".format(dirname(url), str(e)))
    return ""


def download_image(img_tag):
    """From given soup img tag, try to get it's content and save it on a new image file"""
    try:
        print('[+] Dowloading image... {}'.format(img_tag))
        source = img_tag['src']
        content = urllib2.urlopen(source).read()
        filename = basename(urlsplit(content)[2])
        with open(filename, 'wb') as img_file:
            img_file.write(content)
        return filename
    except Exception:
        return ''


def print_exiftool_data(img_filename):
    """From given img filename, print image exiftool GPS info, if there is any"""
    data = {}
    try:
        img_file = Image.open(img_filename)
        info = img_file._getexif()
        if not info:
            return

        for (tag, value) in info.items():
            decoded = TAGS.get(tag, tag)
            data[decoded] = value

        exifGPS = data['GPSInfo']
        if not exifGPS:
            return

        print('[*] "{}" contains GPS MetaData'.format(img_filename))
    except Exception:
        pass


if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog -u <target url>')
    parser.add_option('-u', dest='url', type='string', help='specify url address')

    (options, args) = parser.parse_args()
    url = options.url
    if not url:
        print(parser.usage)
        exit(0)

    # run pipeline
    images = find_images(url)
    print("[*] Found {} images".format(len(images)))
    map(lambda img_tag: print_exiftool_data(download_image(img_tag)), images)
