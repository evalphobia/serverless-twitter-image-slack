import os


def get_search_users():
    if 'TWEET_SEARCH_USERS' in os.environ:
        return os.environ['TWEET_SEARCH_USERS']
    return ''


def get_search_hashtags():
    if 'TWEET_SEARCH_HASHTAGS' in os.environ:
        return os.environ['TWEET_SEARCH_HASHTAGS']
    return ''


def get_search_ignore_words():
    if 'TWEET_SEARCH_IGNORE_WORDS' in os.environ:
        return os.environ['TWEET_SEARCH_IGNORE_WORDS']
    return ''


def get_search_since_min():
    """Past minutes to search tweets. Default 5 minutes."""
    if 'TWEET_SEARCH_SINCE_MIN' in os.environ:
        return os.environ['TWEET_SEARCH_SINCE_MIN']
    return 5


def get_slack_user_name():
    if 'SLACK_USERNAME' in os.environ:
        return os.environ['SLACK_USERNAME']
    return None


def get_slack_channel():
    if 'SLACK_CHANNEL' in os.environ:
        return os.environ['SLACK_CHANNEL']
    return None


def get_slack_url():
    if 'SLACK_URL' in os.environ:
        return os.environ['SLACK_URL']
    if 'SLACK_WEBHOOK_URL' in os.environ:
        return os.environ['SLACK_WEBHOOK_URL']
    raise Exception("[ENV Error] you must set 'SLACK_WEBHOOK_URL'")
