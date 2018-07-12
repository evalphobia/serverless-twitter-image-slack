"""
Search images from Twitter with query.

Most of code for searching Twitter are from Jefferson Henrique's GetOldTweets-python.
- https://github.com/Jefferson-Henrique/GetOldTweets-python
"""
from datetime import datetime
import logging
import re
import requests
from bs4 import BeautifulSoup, FeatureNotFound

import got

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATE_FORMAT = '%Y-%m-%d'
reURL = re.compile('pic.twitter.com/[^ ]+')


def search_by_params(dt, users='', hashtags='', ignores=''):
    target_query = _get_target_query(users, hashtags, ignores)
    query = '%s since:%s filter:media' % (target_query, dt.strftime(DATE_FORMAT))
    tweets = search(query)

    results = []
    for tweet in tweets:
        tweeted_at = datetime.strptime(tweet['datetime'], '%Y-%m-%d %H:%M:%S')
        if tweeted_at > dt:
            results.append(tweet)

    return results


def _get_target_query(users, hashtags, ignores):
    query = ''
    user_list = _get_user_list(users)
    hashtag_list = _get_hashtag_list(hashtags)
    user_list.extend(hashtag_list)
    if len(user_list) != 0:
        query = '(%s)' % ' OR '.join(user_list)

    ignore_list = _get_ignore_list(ignores)
    if len(ignore_list) != 0:
        query += ' %s' % ' '.join(ignore_list)
    return query


def _get_user_list(users):
    user_list = []
    for u in users.split(','):
        u = u.strip()
        if u == '':
            continue
        if u[0] != '@':
            u = ('@%s' % u)
        user_list.append('from:%s' % u)
    return user_list


def _get_hashtag_list(hashtags):
    hashtag_list = []
    for tag in hashtags.split(','):
        tag = tag.strip()
        if tag == '':
            continue
        if tag[0] != '#':
            tag = ('#%s' % tag)
        hashtag_list.append('%s' % tag)
    return hashtag_list


def _get_ignore_list(ignores):
    ignore_list = []
    for ignore in ignores.split(','):
        ignore = ignore.strip()
        if ignore == '':
            continue
        if ignore[0] != '-':
            ignore = ('-%s' % ignore)
        ignore_list.append('%s' % ignore)
    return ignore_list


def search(q):
    result = []
    tweetCriteria = got.manager.TweetCriteria()
    tweetCriteria.querySearch = q

    logger.info('[tweet.search] search: query=[%s]' % q)

    def receiveBuffer(tweets):
        for t in tweets:
            data = {
                'id': t.id,
                'user_id': t.author_id,
                'username': t.username,
                'date': t.date.strftime("%Y-%m-%d"),
                'datetime': t.date.strftime("%Y-%m-%d %H:%M:%S"),
                'retweets': t.retweets,
                'favorites': t.favorites,
                'text': t.text,
                'mentions': t.mentions,
                'hashtags': t.hashtags,
                'permalink': t.permalink,
            }
            if t.geo:
                data['geo'] = t.geo
            if t.mentions:
                data['mentions'] = t.mentions
            if t.hashtags:
                data['hashtags'] = t.hashtags

            result.append(data)
        logger.info('[TWEET] searched %d tweets...' % len(tweets))

    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
    return result


def get_tweet_pic_url(tweets):
    """Get image's tweet URL from tweets"""
    results = []
    for t in tweets:
        m = reURL.search(t['text'])
        if m is not None:
            results.append('https://%s' % m.group())
    logger.info('[tweet.get_tweet_pic_url] results: [%s]' % results)
    return results


def get_images(urls):
    """Get image src URL list from Tweet URL list"""
    results = []
    for url in urls:
        soup = _prepare_scraping(url)
        if _has_video(soup):
            results.append({'url': url, 'image': None})
            continue

        image = _get_image_url(soup)
        logger.info('[tweet._get_image_url_from_tweet] url=[%s], image=[%s]' % (url, image))
        if image:
            results.append({'url': url, 'image': image})
    logger.info('[tweet.get_images] results: [%s]' % results)
    return results


def _prepare_scraping(url):
    """Scraping from tweet URL"""
    resp = requests.get(url)
    try:
        soup = BeautifulSoup(resp.text, 'lxml')
    except FeatureNotFound:
        soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def _has_video(soup):
    """Check video tags"""
    return soup.select_one('.AdaptiveMedia-video') is not None


def _get_image_url(soup):
    """Select image src URL"""
    return soup.select_one('img[data-aria-label-part]').get('src').strip()
