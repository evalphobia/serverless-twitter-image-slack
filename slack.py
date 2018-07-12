import json
import logging
from urllib.request import Request, urlopen, URLError, HTTPError

import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_text_to_slack(tweet):
    req = Request(config.get_slack_url(), _get_request_params(tweet['url'], tweet['image']))
    try:
        response = urlopen(req)
        response.read()
        logger.info('Message posted.')
    except HTTPError as e:
        logger.error('Request failed: %d %s', e.code, e.reason)
    except URLError as e:
        logger.error('Server connection failed: %s', e.reason)


def _get_request_params(url, image):
    params = {
        'channel': config.get_slack_channel(),
    }

    if image is None:
        params['text'] = url
    else:
        params['attachments'] = [
            {'text': url, 'image_url': image}
        ]

    user = config.get_slack_user_name()
    if user is not None:
        params['username'] = user
    return json.dumps(params).encode('utf-8')
