from datetime import datetime, timedelta

import config
import tweet
import slack


def handler(event, context):
    """Search twitter and save result."""
    dt = _get_search_datetime()
    users = config.get_search_users()
    hashtags = config.get_search_hashtags()
    ignores = config.get_search_ignore_words()

    result = tweet.search_by_params(dt, users, hashtags, ignores)
    if len(result) == 0:
        return

    urls = tweet.get_tweet_pic_url(result)
    image_tweets = tweet.get_images(urls)
    for t in image_tweets:
        slack.send_text_to_slack(t)


def _get_search_datetime():
    minute = config.get_search_since_min()
    dt = datetime.now() - timedelta(minutes=int(minute))
    return dt


if __name__ == '__main__':
    handler(None, None)
