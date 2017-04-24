#!/usr/bin/env python

from __future__ import unicode_literals
# from PyCRC.CRC16 import CRC16

import requests
import re
import hashlib
import base64


def debugMode(baseurl, session, option):
    data = '<request><mode>%d</mode></request>' % option
    # r= session.post(baseurl + "api/device/mode", data=data)
    r = session.get(baseurl + "api/global/module-switch")
    #r = session.get(baseurl + "config/global/config.xml")
    print(r.text)


def login(baseurl, username, password):
    s = requests.Session()
    r = s.get(baseurl + "html/home.html")
    # print r.text
    csrf_tokens = grep_csrf(r.text)
    headers_update(s.headers, csrf_tokens[1])
    data = login_data(username, password, str(csrf_tokens[1]))
    r = s.request('POST', baseurl + "api/user/login", data=data)
    print(r.text)
    s.headers.update({'__RequestVerificationToken': r.headers["__requestverificationtokenone"]})
    print(r.text)
    return s


def headers_update(dictbase, token):
    dictbase['Accept-Language'] = 'en-US'
    dictbase['Content-Type'] = 'application/x-www-form-urlencoded'
    dictbase['X-Requested-With'] = 'XMLHttpRequest'
    dictbase['__RequestVerificationToken'] = token
    dictbase['Cache-Control'] = 'no-cache'
    dictbase[
        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'


def grep_csrf(html):
    pat = re.compile(r".*meta name=\"csrf_token\" content=\"(.*)\"", re.I)
    matches = (pat.match(line) for line in html.splitlines())
    return [m.group(1) for m in matches if m]


def login_data(username, password, csrf_token):
    def encrypt(text):
        m = hashlib.sha256()
        m.update(text.encode('ascii'))
        return base64.b64encode(m.hexdigest().encode('ascii')).decode('ascii')

    password_hash = encrypt(username + encrypt(password) + csrf_token)
    return '<?xml version "1.0" encoding="UTF-8"?><request><Username>%s</Username><Password>%s</Password><password_type>4</password_type></request>' % (
        username, password_hash)


baseurl = "http://192.168.174.1/"
username = "admin"
password = "andyromyandy1"

if __name__ == "__main__":
    print("Trying to log in...")
    s = login(baseurl, username, password)
    print("Logged in!!")
    debugMode(baseurl, s, 4)
