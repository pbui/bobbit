# feeds.py

import datetime
import dbm.gnu
import collections
import logging
import uuid
import time

import aiohttp
import feedparser

from bobbit.message import Message
from bobbit.utils   import shorten_url, strip_html

# Metadata

NAME     = 'feeds'
ENABLE   = True
TEMPLATE = 'From {color}{green}{feed}{color} feed: {bold}{title}{bold} by {color}{cyan}{author}{color} @ {color}{blue}{link}{color}'

# Utilities

async def process_feed(http_client, feed, cache):
    feed_title    = feed['title']
    feed_url      = feed['url']
    feed_channels = feed['channels']
    feed_key      = feed_title.encode('ascii', 'ignore')

    logging.debug('Fetching %s (%s)', feed_title, feed_url)
    try:
        if 'nonce' in feed_url:
            feed_url = feed_url.format(nonce=uuid.uuid4())

        # Set If-Modified-Since Header to be nice...
        if feed_key in cache:   # A week before last entry
            last_modified = datetime.datetime.fromtimestamp(float(cache[feed_key]) - 7*24*60*60)
        else:                   # A month ago
            last_modified = datetime.datetime.fromtimestamp(time.time() - 30*24*60*60)

        headers = {'If-Modified-Since': last_modified.strftime('%a, %d %b %Y %X GMT')}
        async with http_client.get(feed_url, headers=headers) as response:
            feed_content = await response.content.read()
    except aiohttp.client_exceptions.ClientPayloadError as e:
        logging.warning('Could not fetch %s: %s', feed_url, e)
        return

    last_modified = time.time()

    logging.debug('Parsing %s (%s)', feed_title, feed_url)
    for entry in feedparser.parse(feed_content)['entries']:
        link   = entry.get('link', '')
        title  = strip_html(entry.get('title', ''))
        key    = link.encode('ascii','ignore')

        # Workaround long authorship in The Conversation, FiveThirtyEight
        author = entry.get('author', 'Unknown').split(',')[0].split('(')[0].strip()
        if 'author' in feed:
            author = feed['author'].format(author=author)

        # If link starts with //, replace with https:// (workaround for the Week bug)
        if link.startswith('//'):
            link = 'https:' + link

        # If there is no key, then skip
        if not key:
            logging.debug('No key for %s', link)
            continue

        # If key is in cache and the timestamp is > 1.0, then skip
        if key in cache and float(cache[key]) > 1.0:
            logging.debug('Skipping %s (already %s)', link, cache[key].decode())
            continue

        # If feed is not in cache, then it is new, so mark all entries as skipped
        if feed_key not in cache:
            logging.debug('Skipping %s (new feed)', link)
            cache[key] = str(time.time())
            continue

        # If date published is too old, then mark and skip recording
        timestamp = entry.get('updated_parsed', entry.get('published_parsed', None))
        timestamp = time.mktime(timestamp) if timestamp else time.time()
        time_diff = time.time() - timestamp
        if time_diff > 24*60*60: # One day
            logging.debug('Skipping %s (too old)', link)
            cache[key] = str(time.time())
            continue

        # If date published is in the future (half a day), then skip for now
        if time_diff < -12*60*60:
            logging.debug('Skipping %s (in the future)', link)
            continue

        # Record entry with a key of 1.0 and then add to list of items
        logging.debug('Recording %s', link)
        cache[key] = str(1.0)
        yield {
            'title'     : title,
            'author'    : author,
            'link'      : link,
            'channels'  : feed_channels,
            'timestamp' : timestamp,
        }

        # Set last modified time to minimum of current time and entry timestamp
        last_modified = min(last_modified, timestamp)

    # Mark feed in cache
    cache[feed_key] = str(last_modified)

# Timer

async def feeds_timer(bot):
    logging.info('Feeds timer starting...')

    # Read configuration
    config           = bot.config.load_module_config('feeds')
    templates        = config.get('templates', {})
    default_template = templates.get('default', TEMPLATE)

    # Read and process results
    entries       = collections.defaultdict(list)
    entries_limit = config.get('limit', 5)
    cache_path    = bot.config.get_config_path('feeds.cache')

    with dbm.open(cache_path, 'c') as cache:
        logging.debug('Processing feeds...')
        for feed in config['feeds']:
            feed_title = feed['title']

            try:
                async for feed_entry in process_feed(bot.http_client, feed, cache):
                    entries[feed_title].append(feed_entry)
            except Exception as e:
                logging.warning('Unable to process feed %s: %s', feed_title, e)

        logging.debug('Delivering feeds...')
        for feed_title, entries in entries.items():
            logging.debug('Delivering %s...', feed_title)
            for index, entry in enumerate(sorted(entries, key=lambda e: e['timestamp'])):
                if index > entries_limit:   # Enforce entries limit
                    break

                title    = entry['title'].replace('\r', ' ').replace('\n', ' ')
                key      = entry['link'].encode('ascii', 'ignore')
                link     = await shorten_url(bot.http_client, entry['link'])
                author   = entry['author']
                channels = entry['channels']

                logging.debug('Delivering %s...', title)

                # Send each entry to the appropriate channel
                for channel in channels:
                    template = templates.get(channel, default_template)
                    await bot.outgoing.put(Message(
                        channel = channel,
                        body    = bot.client.format_text(
                            template,
                            feed   = feed_title,
                            title  = title,
                            link   = link,
                            author = author
                        )
                    ))

                # Mark entry as delivered
                logging.info(
                    'Delivered %s from %s to %s',
                    title, feed_title, ', '.join(channels)
                )
                cache[key] = str(time.time())

# Register

def register(bot):
    config  = bot.config.load_module_config('feeds')
    timeout = config.get('timeout', 5*60)

    if not config:
        return []

    return (
        ('timer', timeout, feeds_timer),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
