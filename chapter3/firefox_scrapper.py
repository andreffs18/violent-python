#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import sqlite3
import optparse
from functools import wraps

FOLDERS = [
    "Library/Application Support/Firefox/Profiles/",
    "Library/Mozilla/Firefox/Profiles/"
]


def sqlite3_except(func):
    @wraps(func)
    def wrapper(db):
        try:
            return func(db)
        except Exception as e:
            if "encrypted" in str(e):
                print("[*] Error reading your cookies database. (Upgrade your Python-Sqlite3 Library)")
    return wrapper


@sqlite3_except
def print_downloads(download_db):
    conn = sqlite3.connect(download_db)
    c = conn.cursor()
    c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') '
              'FROM moz_downloads;')
    print("[*] --- Files Downloaded ---")
    for row in c:
        row = map(str, row)
        print("[+] File: {} from source: {} at: {}".format(*row))


@sqlite3_except
def print_cookies(cookies_db):
    conn = sqlite3.connect(cookies_db)
    c = conn.cursor()
    c.execute('SELECT host, name, value '
              'FROM moz_cookies')
    print("[*] --- Found Cookies ---")
    for row in c:
        row = map(str, row)
        print("[+] Host: {}, Cookie: {}, Value: {}".format(*row))


@sqlite3_except
def print_history(places_db):
    conn = sqlite3.connect(places_db)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') "
              "FROM moz_places, moz_historyvisits "
              "WHERE visit_count > 0 AND moz_places.id==moz_historyvisits.place_id;")
    print("[*] --- Found History ---")
    for row in c:
        row = map(str, row)
        print("[+] {} - Visited: {}".format(*row))


@sqlite3_except
def print_google(places_db):
    conn = sqlite3.connect(places_db)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') "
              "FROM moz_places, moz_historyvisits "
              "WHERE visit_count > 0 AND moz_places.id==moz_historyvisits.place_id;")

    print("[*] --- Found Google ---")
    for row in c:
        row = map(str, row)
        url = row[0].lower()
        date = row[1]

        if 'google' not in url.lower():
            continue
        r = re.findall(r'q=.*\&', url)
        if not r:
            continue

        search = r[0].split('&')[0]
        search = search.replace("q=", "").replace("+", " ")
        print("[+] {} - Searched For: \"{}\"".format(date, search))


def get_existing_profiles():
    # search for all users under /Users/ directories
    profiles = []

    home = os.path.expanduser("~")
    folders = map(lambda folder: os.path.join(home, folder), FOLDERS)
    for folder in folders:
        # check if folder exist, if so, how many profiles are inside
        print("[*] Folder {}...".format(folder))
        if not os.path.isdir(folder):
            print("[-] No profiles found")
            continue

        for name in os.listdir(folder):
            profile_path = os.path.join(folder, name)
            if os.path.isdir(profile_path):
                print("[+] Profile \"{}\" found: {}".format(name, profile_path))
                profiles.append(profile_path)

    if not profiles:
        return None

    print("[+] Using first profile found \"{}\"".format(profiles[0]))
    return profiles[0]


if __name__ == '__main__':
    parser = optparse.OptionParser("usage %prog -p <firefox profile path> ")
    parser.add_option('-p', dest='path_name', type='string', help='specify firefox profile path')

    (options, args) = parser.parse_args()

    path_name = options.path_name
    if not path_name:
        print(parser.usage)
        print("[*] No profile folder was given. Searching for profiles...")
        path_name = get_existing_profiles()
        if not path_name:
            exit(0)

    if not os.path.isdir(path_name):
        print("[!] Path Does Not Exist: {}".format(path_name))
        exit(0)

    download_db = os.path.join(path_name, 'downloads.sqlite')
    if os.path.isfile(download_db):
        print_downloads(download_db)
    else:
        print("[!] Downloads DB does not exist: {}".format(download_db))

    cookies_db = os.path.join(path_name, 'cookies.sqlite')
    if os.path.isfile(cookies_db):
        print_cookies(cookies_db)
    else:
        print("[!] Cookies DB does not exist: {}".format(cookies_db))

    places_db = os.path.join(path_name, 'places.sqlite')
    if os.path.isfile(places_db):
        print_history(places_db)
        print_google(places_db)
    else:
        print("[!] PlacesDb does not exist: {}".format(places_db))



