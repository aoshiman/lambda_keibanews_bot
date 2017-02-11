## -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import yaml
import lamvery

FILE = 'keibanews.txt'
URL = 'http://keiba.radionikkei.jp/keiba/rss2/news/'
BUCKET = 'keibanews.aoshiman.org'

try:
    with open(lamvery.secret.file('config.yml')) as f:
    #  with open('config.yml') as f:
        _oauth_conf = yaml.load(f)

except Exception as e:
    print(e)

CONSUMER_KEY = _oauth_conf['consumer_key']
CONSUMER_SECRET = _oauth_conf['consumer_secret']
ACCESS_TOKEN = _oauth_conf['access_token']
ACCESS_SECRET = _oauth_conf['access_secret']
