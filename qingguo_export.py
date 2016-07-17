#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urlparse import urlparse
import os

import config


def download_url_to_file(url, filename):
    dest = os.path.join(config.DOWNLOAD_DIR, filename)
    if os.path.exists(dest):
        return 'Skip!'
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Exception('HTTP ERROR %d', r.status_code)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    return 'Success!'
    

def main():
    if not os.path.isdir(config.DOWNLOAD_DIR):
        print 'Error: %s is not exists or not a directory!' % config.DOWNLOAD_DIR
        return

    cookies = {
        'smartcamera_buy_pc_fg_sessionid': config.SESSION_ID
    }
    payload = {
        'deviceId': config.DEVICE_ID,
        'limit': 65535,
        'offset': 0,
        'searchTime': -1,
        'from': '',
        'to': ''
    }
    r = requests.post("https://x.163.com/live/fgadmin/record/list",
                      cookies=cookies, json=payload)
    list_result = r.json()
    print 'Found %d videos, start download videos...' % list_result['size']
    i = 1
    for rec in list_result['records']:
        print 'Download %d/%d...' % (i, list_result['size']),
        url = rec['url']
        o = urlparse(url)
        filename = os.path.basename(o.path)
        try:
            ret = download_url_to_file(url, filename)
        except Exception as e:
            print 'Error: %s' % e
            return
        print ret
        i += 1
    print 'All video downloaded successfully! Cool!'


if __name__ == '__main__':
    main()
