# tweets.py

import dbm.gnu
import collections
import hashlib
import json
import logging
import os
import sys
import time

import lxml.html
import twitter
import yaml

import tornado.gen
import tornado.httpclient
import tornado.options
import tornado.process

# Metadata

NAME     = 'tweets'
ENABLE   = True
TYPE     = 'timer'
TEMPLATE = 'From "{user}" twitter: {text}'

# Timer

@tornado.gen.coroutine
def timer(bot):
    # Execute tweets script
    bot.logger.info('Executing %s', __file__)
    command = ['python3', __file__, '--config-dir={}'.format(bot.config_dir)]
    process = tornado.process.Subprocess(command, stdout=tornado.process.Subprocess.STREAM)
    results = yield tornado.gen.Task(process.stdout.read_until_close)

    # Read and process results
    for user, entries in json.loads(results).items():
        for entry in entries:
            text     = entry['text']
            channels = entry['channels']
            message  = TEMPLATE.format(user=user, text=text)

            # Send each entry to the appropriate channel
            for channel in channels:
                bot.send_message(message, channel=channel)

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
            # Update since_id
            tweets_cache['since_id'] = str(max(int(tweets_cache['since_id']), status.id))

            # Skip if message is older than timeout
            if current_time - status.created_at_in_seconds >= tweets_timeout:
                logger.debug('Skipping message from %s (too old)', user)
                continue

            # Skip if message does not contain pattern
            status_text = strip_html(status.text)
            if pattern and pattern not in status_text:
                logger.debug("Skipping message from %s (doesn't match pattern)", user)
                continue

            # Skip if message is in cache
            status_key = '{}/{}'.format(user.lower(), status.id)
            if status_key in tweets_cache:
                logger.debug('Skipping message from %s (in cache)', user)
                continue

            # Mark message in cache
            tweets_cache[status_key] = str(time.time())

            # Add message to entries
            logger.debug('Recording message from %s: %s', user, status_text)
            entries[user].append({
                'text'     : status_text,
                'channels' : channels,
            })

    # Dump entries as JSON
    json.dump(entries, sys.stdout)

# Utilities

def strip_html(s):
    try:
        return lxml.html.fromstring(s).text_content()
    except lxml.etree.XMLSyntaxError:
        return s

# Main Execution

if __name__ == '__main__':
    tornado.options.define('config_dir', default=None,  help='Configuration directory')
    tornado.options.parse_command_line()
    options = tornado.options.options.as_dict()

    try:
        script(os.path.expanduser(options.get('config_dir', '~/.config/bobbit')))
    except Exception as e:
        logging.getLogger().warn(e)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
