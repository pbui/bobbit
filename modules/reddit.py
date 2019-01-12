# reddit.py

from modules.__common__ import shorten_url

import json

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'reddit'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!reddit (?P<subreddit>[^\s]*)\s*(?P<query>.*)$'
USAGE   = '''Usage: !reddit <subreddit> [<query>]
Given a subreddit, this returns an article from the subreddit that match the
query.
Example:
    > !reddit linuxmasterrace
'''

# Constants

REDDIT_TEMPLATE = 'http://reddit.com/r/{subreddit}/.json'

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, subreddit, query=''):
    url    = REDDIT_TEMPLATE.format(subreddit=subreddit)
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)
    query  = query.lower()

    try:
        for result in json.loads(result.body.decode())['data']['children']:
            data  = result['data']
            title = data['title']
            url   = data['url']
            nsfw  = '[NSFW] ' if data['over_18'] else ''

            if query not in title.lower() and query not in url.lower():
                continue

            if data['stickied']:
                continue

            response = 'From {} - {}{} @ {}'.format(subreddit, nsfw, title, url)
            shorturl = yield shorten_url(url)
            if url != shorturl:
                response += ' || ' + shorturl
            break
    except (IndexError, KeyError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
