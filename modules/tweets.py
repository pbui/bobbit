# tweets.py

import dbm.gnu
import collections
import json
import logging
import os
import sys
import time

import twitter
import yaml

import tornado.gen
import tornado.httpclient
import tornado.options
import tornado.process

from modules.__common__ import shorten_url, strip_html

# Metadata

NAME     = 'tweets'
ENABLE   = True
TYPE     = 'timer'
TEMPLATE = 'From {color}{green}{user}{color} twitter: {bold}{status}{bold} @ {color}{blue}{link}{color}'

# Timer

@tornado.gen.coroutine
def timer(bot):
    # Execute tweets script
    bot.logger.info('Executing %s', __file__)
    command = ['python3', __file__, '--config-dir={}'.format(bot.config_dir)]
    environ = dict(os.environ, **{'PYTHONPATH': os.path.join(__file__, '..', '..') + ':' + os.environ.get('PYTHONPATH', '')})
    process = tornado.process.Subprocess(command, stdout=tornado.process.Subprocess.STREAM, env=environ)
    results = yield tornado.gen.Task(process.stdout.read_until_close)

    # Read configuration
    config_path      = os.path.join(bot.config_dir, 'tweets.yaml')
    tweets_config    = yaml.load(open(config_path))
    templates        = tweets_config.get('templates', {})
    default_template = templates.get('default', TEMPLATE)

    # Read and process results
    cache_path = os.path.join(bot.config_dir, 'tweets.cache')
    with dbm.open(cache_path, 'c') as tweet_cache:
        for user, entries in json.loads(results).items():
            for entry in entries:
                status      = entry['status']
                channels    = entry['channels']
                status_key  = entry['status_key']
                status_id   = entry['status_id']
                link        = yield shorten_url(entry['link'])

                # Send each entry to the appropriate channel
                for channel in channels:
                    template = templates.get(channel, default_template)
                    message  = bot.format_text(template, user=user, status=status, link=link)
                    bot.send_message(message, channel=channel)

                # Mark entry as delivered
                bot.logger.info('Delivered %s from %s to %s', status, user, ', '.join(channels))
                tweet_cache['since_id'] = str(max(int(tweet_cache['since_id']), status_id))
                tweet_cache[status_key] = str(time.time())

# Register

def register(bot):
    config_path   = os.path.join(bot.config_dir, 'tweets.yaml')
    tweets_config = yaml.load(open(config_path))
    timeout       = tweets_config.get('timeout', 5*60)

    return (
        (timeout, timer),
    )

# Script

def script(config_dir):
    # Open configuration
    config_path    = os.path.join(config_dir, 'tweets.yaml')
    tweets_config  = yaml.load(open(config_path))
    tweets_timeout = tweets_config.get('timeout', 5*60)

    # Open cache
    cache_path     = os.path.join(config_dir, 'tweets.cache')
    tweets_cache   = dbm.open(cache_path, 'c')

    # Load Twitter API
    twitter_api = twitter.Api(
        cache               = None,
        consumer_key        = tweets_config['consumer_key'],
        consumer_secret     = tweets_config['consumer_secret'],
        access_token_key    = tweets_config['access_token_key'],
        access_token_secret = tweets_config['access_token_secret'],
    )

    # Read tweets
    entries      = collections.defaultdict(list)
    current_time = time.time()
    logger       = logging.getLogger()

    try:
        since_id = int(tweets_cache['since_id'])
    except:
        since_id = 0

    tweets_cache['since_id'] = str(since_id)

    for feed in tweets_config['feeds']:
        user     = feed['user']
        channels = feed['channels']
        pattern  = feed.get('pattern', '')

        logger.info('Fetching %s timeline', user)
        try:
            statuses = twitter_api.GetUserTimeline(screen_name=user, trim_user=True, include_rts=False, exclude_replies=True, since_id=since_id)
        except twitter.error.TwitterError:
            logger.warn('Could not get timeline for %s', user)
            continue

        for status in statuses:
            # Skip if status is older than timeout
            if current_time - status.created_at_in_seconds >= tweets_timeout:
                logger.debug('Skipping status from %s (too old)', user)
                continue

            # Skip if status does not contain pattern
            status_text = strip_html(status.text)
            if pattern and pattern not in status_text:
                logger.debug("Skipping status from %s (doesn't match pattern)", user)
                continue

            # Skip if status is in cache
            status_key = '{}/{}'.format(user.lower(), status.id)
            if status_key in tweets_cache:
                logger.debug('Skipping status from %s (in cache)', user)
                continue

            # Add status to entries
            logger.debug('Recording status from %s: %s', user, status_text)
            entries[user].append({
                'status'    : status_text,
                'channels'  : channels,
                'status_key': status_key,
                'status_id' : status.id,
                'link'      : 'https://twitter.com/{}/status/{}'.format(user, status.id),
            })

    # Dump entries as JSON
    json.dump(entries, sys.stdout)

# Main Execution

if __name__ == '__main__':
    tornado.options.define('config_dir', default=None,  help='Configuration directory')
    tornado.options.parse_command_line()
    options = tornado.options.options.as_dict()

    script(os.path.expanduser(options.get('config_dir', '~/.config/bobbit')))

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
