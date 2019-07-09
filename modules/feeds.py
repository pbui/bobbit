# feeds.py

import dbm.gnu
import collections
import json
import logging
import os
import sys
import time

import feedparser
import yaml

import tornado.gen
import tornado.httpclient
import tornado.options
import tornado.process

# Metadata

NAME     = 'feeds'
ENABLE   = True
TYPE     = 'timer'
TEMPLATE = 'From "{feed}" feed: {title} by {author} @ {link}'

# Timer

@tornado.gen.coroutine
def timer(bot):
    from modules.__common__ import shorten_url

    # Execute feeds script
    bot.logger.info('Executing %s', __file__)
    command = ['python3', __file__, '--config-dir={}'.format(bot.config_dir)]
    process = tornado.process.Subprocess(command, stdout=tornado.process.Subprocess.STREAM)
    results = yield tornado.gen.Task(process.stdout.read_until_close)

    # Read configuration
    config_path  = os.path.join(bot.config_dir, 'feeds.yaml')
    feeds_config = yaml.load(open(config_path))
    templates    = feeds_config.get('templates', {})

    # Read and process results
    cache_path = os.path.join(bot.config_dir, 'feeds.cache')

    with dbm.open(cache_path, 'c') as feeds_cache:
        for feed, entries in json.loads(results).items():
            for entry in entries:
                title    = entry['title'].replace('\r', ' ').replace('\n', ' ')
                key      = entry['link'].encode('ascii', 'ignore')
                link     = yield shorten_url(entry['link'])
                author   = entry['author']
                channels = entry['channels']

                # Send each entry to the appropriate channel
                for channel in channels:
                    template = templates.get(channel, TEMPLATE)
                    message  = template.format(feed=feed, title=title, link=link, author=author)
                    bot.send_message(message, channel=channel)

                # Mark entry as delivered
                bot.logger.info('Delivered %s from %s to %s', title, feed, ', '.join(channels))
                feeds_cache[key] = str(time.time())

# Register

def register(bot):
    config_path  = os.path.join(bot.config_dir, 'feeds.yaml')
    feeds_config = yaml.load(open(config_path))
    timeout      = feeds_config.get('timeout', 5*60)

    return (
        (timeout, timer),
    )

# Script

def script(config_dir):
    config_path  = os.path.join(config_dir, 'feeds.yaml')
    feeds_config = yaml.load(open(config_path))

    cache_path   = os.path.join(config_dir, 'feeds.cache')
    feeds_cache  = dbm.open(cache_path, 'c')

    entries      = collections.defaultdict(list)
    entries_limit= feeds_config.get('limit', 5)
    logger       = logging.getLogger()

    for feed_config in feeds_config['feeds']:
        feed_title    = feed_config['title']
        feed_url      = feed_config['url']
        feed_channels = feed_config['channels']
        feed_key      = feed_title.encode('ascii', 'ignore')

        logger.info('Fetching %s (%s)', feed_title, feed_url)

        client  = tornado.httpclient.HTTPClient()
        request = tornado.httpclient.HTTPRequest(feed_url, request_timeout=10)
        try:
            result = client.fetch(request)
        except Exception as e:
            logger.warning(e)
            continue

        logger.info('Parsing %s (%s)', feed_title, feed_url)

        for entry in feedparser.parse(result.body)['entries']:
            link   = entry.get('link', '')
            title  = entry.get('title', '')
            author = entry.get('author', 'Unknown')
            key    = link.encode('ascii','ignore')

            # If there is no key, then skip
            if not key:
                logger.debug('No key for %s', link)
                continue

            # If key is in cache and the timestamp is > 1.0, then skip
            if key in feeds_cache and float(feeds_cache[key]) > 1.0:
                logger.debug('Skipping %s (already %s)', link, feeds_cache[key].decode())
                continue

            # If feed is not in cache, then it is new, so mark all entries as skipped
            if feed_key not in feeds_cache:
                logger.debug('Skipping %s (new feed)', link)
                feeds_cache[key] = str(time.time())
                continue

            # If date published is too old, then mark and skip recording
            timestamp = entry.get('updated_parsed', entry.get('published_parsed', None))
            timestamp = time.mktime(timestamp) if timestamp else time.time()
            if time.time() - timestamp > 24*60*60:
                logger.debug('Skipping %s (too old)', link)
                feeds_cache[key] = str(time.time())
                continue

            # Record entry with a key of 1.0 and then add to list of items
            logger.info('Recording %s', link)
            feeds_cache[key] = str(1.0)
            entries[feed_title].append({
                'title'     : title,
                'author'    : author,
                'link'      : link,
                'channels'  : feed_channels,
                'timestamp' : timestamp,
            })

        # Mark feed in cache
        feeds_cache[feed_key] = str(time.time())

        # Only report up to rss_limit entries for this feed
        entries[feed_title] = entries[feed_title][0:entries_limit]

    for feed_title, feed_entries in entries.items():
        entries[feed_title] = list(sorted(feed_entries, key=lambda e: e['timestamp']))

    json.dump(entries, sys.stdout)

# Main Execution

if __name__ == '__main__':
    tornado.options.define('config_dir', default=None,  help='Configuration directory')
    tornado.options.parse_command_line()
    options = tornado.options.options.as_dict()

    try:
        script(os.path.expanduser(options.get('config_dir', '~/.config/bobbit')))
    except Exception as e:
        logging.getLogger().warning(e)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
