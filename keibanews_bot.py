# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from time import localtime, mktime, strftime
import email.utils
import feedparser
from twython import Twython, TwythonError
from boto3 import Session
from setting import (CONSUMER_KEY, CONSUMER_SECRET,
                     ACCESS_TOKEN, ACCESS_SECRET, URL, BUCKET)


def parse_feed(u):
    data = feedparser.parse(u)
    feed = []
    for entry in data.entries:
        feed.append([entry.published, entry.title, entry.link])
    feed.reverse()
    return feed


def get_news_list(bucket):
    s3 = Session().resource('s3')
    bucket = s3.Bucket(bucket)
    return [obj.key for obj in bucket.objects.all()]


def put_news(bucket, keyname):
    s3 = Session().resource('s3')
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(keyname)
    body = keyname
    response = obj.put(
            Body=body.encode('utf-8'),
            ContentEncoding='utf-8',
            ContentType='text/plane'
            )


def tweet_news():
    """OAuth setting and Twit(if news is new)"""
    twitter = Twython(
                      CONSUMER_KEY,
                      CONSUMER_SECRET,
                      ACCESS_TOKEN,
                      ACCESS_SECRET
                      )

    feed = parse_feed(URL)
    #  print(feed)
    try:
        news_list = get_news_list(BUCKET)
    except:
        pass

    for entry in feed:
        _date, title, url = entry[0], entry[1], entry[2]
        entry_date = strftime('%Y/%m/%d %H:%M',localtime(mktime(email.utils.\
                                                        parsedate(_date))+32400))
        _news_id = url.split('/')
        news_id = _news_id[4]

        if news_id not in news_list:
            post = u'{0} {1} {2}'.format(entry_date, title, url)
            try:
                twitter.update_status(status = post)
                print(post)
            except TwythonError as e:
                print(e)
            finally:
                put_news(BUCKET, news_id)


def lambda_handler(event, context):
    tweet_news()


if __name__ == '__main__':
    tweet_news()
