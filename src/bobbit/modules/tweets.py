# tweets.py

import base64
import dbm.gnu
import collections
import logging
import time

from bobbit.message import Message
from bobbit.utils   import shorten_url

# Metadata

NAME     = 'tweets'
ENABLE   = False
TYPE     = 'timer'
PATTERN  = r'.*twitter.com/[^\s]+/status/(?P<status_id>[0-9]+).*'
TEMPLATE = 'From {color}{green}{user}{color} twitter: {bold}{status}{bold} @ {color}{blue}{link}{color}'

# Constants

TWITTER_USER_TIMELINE_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
TWITTER_STATUSES_SHOW_URL = 'https://api.twitter.com/1.1/statuses/show.json'
TWITTER_OAUTH2_TOKEN_URL  = 'https://api.twitter.com/oauth2/token'

# Utility

async def get_access_token(http_client, key, secret):
    url     = TWITTER_OAUTH2_TOKEN_URL
    token   = base64.b64encode(f'{key}:{secret}'.encode())
    headers = {
        'Authorization' : 'Basic ' + token.decode(),
        'Content-Type'  : 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    params  = {
        'grant_type'    : 'client_credentials'
    }

    async with http_client.post(url, headers=headers, params=params) as response:
        data = await response.json()
        try:
            return data['access_token']
        except KeyError as e:
            logging.exception(e)
            logging.debug(data)
            return None

async def get_user_timeline(http_client, user, since_id, access_token):
    url     = TWITTER_USER_TIMELINE_URL
    headers = {
        'Authorization' : 'Bearer ' + access_token,
    }
    params = {
        'screen_name'    : user,
        'exclude_replies': 'true',
        'trim_user'      : 'true',
        'include_rts'    : 'false',
        'since_id'       : since_id,
        'count'          : 10,
    }

    async with http_client.get(url, headers=headers, params=params) as response:
        return await response.json()

async def process_feed(http_client, feed, cache, access_token):
    user     = feed['user']
    channels = feed['channels']
    pattern  = feed.get('pattern', '')
    since_id = int(cache.get('since_id', 1))
    statuses = await get_user_timeline(http_client, user, since_id, access_token)

    logging.debug('Processing %s timeline...', user)
    for status in statuses:
        # Skip if status does not contain pattern
        status_text = status.get('full_text', status.get('text', '')).replace('\n', ' ')
        if pattern and pattern not in status_text:
            logging.debug("Skipping status from %s (doesn't match pattern)", user)
            continue

        # Skip if status is in cache
        status_key = f'{user.lower()}/{status["id"]}'
        if status_key in cache:
            logging.debug('Skipping status from %s (in cache)', user)
            continue

        # Add status to entries
        logging.debug('Recording status from %s: %s', user, status_text)
        yield {
            'status'    : status_text.replace('\n', ' '),
            'channels'  : channels,
            'status_key': status_key,
            'status_id' : status['id'],
            'link'      : f'https://twitter.com/{user}/status/{status["id"]}'
        }

async def get_status(http_client, status_id, access_token):
    url     = TWITTER_STATUSES_SHOW_URL
    headers = {
        'Authorization' : 'Bearer ' + access_token,
    }
    params = {
        'id'         : status_id,
        'tweet_mode' : 'extended',
    }

    async with http_client.get(url, headers=headers, params=params) as response:
        return await response.json()

# Tweets Title Command

async def tweets_title(bot, message, status_id=None):
    # Read configuration
    config           = bot.config.load_module_config('tweets')
    templates        = config.get('templates', {})
    default_template = templates.get('default', TEMPLATE)

    # Get access token
    access_token = await get_access_token(
        bot.http_client,
        config['consumer_key'],
        config['consumer_secret'],
    )

    status = await get_status(bot.http_client, status_id, access_token)
    text   = status.get('full_text', status.get('text', '')).replace('\n', ' ')
    return message.with_body(bot.client.format_text(
        default_template,
        user   = status['user']['screen_name'],
        status = text,
        link   = await shorten_url(
            bot.http_client,
            f'https://twitter.com/i/web/status/{status_id}'
        )
    ))

# Tweets Timer

async def tweets_timer(bot):
    logging.info('Tweets timer starting...')

    # Read configuration
    config           = bot.config.load_module_config('tweets')
    templates        = config.get('templates', {})
    default_template = templates.get('default', TEMPLATE)

    # Get access token
    access_token = await get_access_token(
        bot.http_client,
        config['consumer_key'],
        config['consumer_secret'],
    )

    # Read tweets
    entries    = collections.defaultdict(list)
    cache_path = bot.config.get_config_path('tweets.cache')

    with dbm.open(cache_path, 'c') as cache:
        logging.debug('Processing tweets...')
        for feed in config.get('feeds', []):
            user = feed['user']
            try:
                async for tweet_entry in process_feed(bot.http_client, feed, cache, access_token):
                    entries[user].append(tweet_entry)
            except Exception as e:
                logging.warning('Unable to process %s feed: %s', user, e)

        logging.debug('Delivering tweets...')
        for user, entries in entries.items():
            for entry in entries:
                status      = entry['status']
                channels    = entry['channels']
                status_key  = entry['status_key']
                status_id   = entry['status_id']
                link        = await shorten_url(bot.http_client, entry['link'])

                # Send each entry to the appropriate channel
                for channel in channels:
                    template = templates.get(channel, default_template)
                    await bot.outgoing.put(Message(
                        channel = channel,
                        body    = bot.client.format_text(
                            template,
                            user   = user,
                            status = status,
                            link   = link,
                        )
                    ))

                # Mark entry as delivered
                logging.info('Delivered %s from %s to %s', status, user, ', '.join(channels))
                cache['since_id'] = str(max(int(cache.get('since_id', 1)), status_id))
                cache[status_key] = str(time.time())

# Register

def register(bot):
    config  = bot.config.load_module_config('tweets')
    timeout = config.get('timeout', 5*60)

    if not config:
        return []

    callbacks = [
        ('timer'  , timeout, tweets_timer),
    ]

    if not config.get('disable_title', False):
        callbacks.append((
            'command', PATTERN, tweets_title
        ))

    return callbacks

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
