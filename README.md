serverless-twitter-image-slack
----

[![License: MIT][3]][4] [![Release][5]][6] [![Build Status][7]][8]  [![Code Climate][19]][20] [![BCH compliance][21]][22]

[3]: https://img.shields.io/badge/License-MIT-blue.svg
[4]: LICENSE.md
[5]: https://img.shields.io/github/release/evalphobia/serverless-twitter-image-slack.svg
[6]: https://github.com/evalphobia/serverless-twitter-image-slack/releases/latest
[7]: https://travis-ci.org/evalphobia/serverless-twitter-image-slack.svg?branch=master
[8]: https://travis-ci.org/evalphobia/serverless-twitter-image-slack
[9]: https://coveralls.io/repos/evalphobia/serverless-twitter-image-slack/badge.svg?branch=master&service=github
[10]: https://coveralls.io/github/evalphobia/serverless-twitter-image-slack?branch=master
[11]: https://codecov.io/github/evalphobia/serverless-twitter-image-slack/coverage.svg?branch=master
[12]: https://codecov.io/github/evalphobia/serverless-twitter-image-slack?branch=master
[15]: https://img.shields.io/github/downloads/evalphobia/serverless-twitter-image-slack/total.svg?maxAge=1800
[16]: https://github.com/evalphobia/serverless-twitter-image-slack/releases
[17]: https://img.shields.io/github/stars/evalphobia/serverless-twitter-image-slack.svg
[18]: https://github.com/evalphobia/serverless-twitter-image-slack/stargazers
[19]: https://codeclimate.com/github/evalphobia/serverless-twitter-image-slack/badges/gpa.svg
[20]: https://codeclimate.com/github/evalphobia/serverless-twitter-image-slack
[21]: https://bettercodehub.com/edge/badge/evalphobia/serverless-twitter-image-slack?branch=master
[22]: https://bettercodehub.com/

`serverless-twitter-image-slack` search tweet with image and post it to Slack channel, powered by AWS Lambda.

# Download

Download serverless-twitter-image-slack by command below.

```bash
$ git clone https://github.com/evalphobia/serverless-twitter-image-slack
$ cd serverless-twitter-image-slack
$ npm install
```

# Config

## serverless.yml

Change environment variables below,

```bash
$ cp serverless.yml.example serverless.yml
$ vim serverless.yml

------------

functions:
  # Change function name, if you don't collect kitten images.
  tweet_cat:
    handler: handler.handler
    memorySize: 128
    timeout: 60
    environment:
      ######### Change here! ########
      TWEET_SEARCH_USERS: "@Number10cat,@catsofinstagram"
      TWEET_SEARCH_SINCE_MIN: 5
      SLACK_USERNAME: twitter-image-bot
      SLACK_CHANNEL: general
      SLACK_WEBHOOK_URL: https://hooks.slack.com/services/XXX/YYY/ZZZ
    events:
      - schedule: cron(*/5 * * * ? *)  # exec every 5min
```

## Environment variables

|Name|Description|Default|
|:--|:--|:--|
| `TWEET_SEARCH_USERS` | The Twitter username. Put multiple user with comma. | - |
| `TWEET_SEARCH_SINCE_MIN` | The threshold time of tweets. | 5 (5min) |
| `SLACK_USERNAME` | Slack webhook username | (Optional) |
| `SLACK_CHANNEL` | Slack webhook channel | (Optional) |
| `SLACK_WEBHOOK_URL` | Slack webhook URL | - |


# Deploy

```bash
# To use `sls` command, install first.
# $ npm install -g serverless

$ AWS_ACCESS_KEY_ID=<...> AWS_SECRET_ACCESS_KEY=<...> sls deploy -v
```


# Check Log

```bash
$ AWS_ACCESS_KEY_ID=<...> AWS_SECRET_ACCESS_KEY=<...> sls logs -f sls-twitter-image-slack -t
```


# Credit

The codebase to get data from Twitter is from [Jefferson-Henrique](https://github.com/Jefferson-Henrique)'s [GetOldTweets-python](https://github.com/Jefferson-Henrique/GetOldTweets-python).
Many thanks!
