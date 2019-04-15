# copypasta.py

# module for bobbit that pulls posts from r/copypasta
# i don't claim any responsibility for the content of the posts
# Gavin Inglis

import os
import re
import random

import tornado.gen
import tornado.httpclient
import json

# Metadata

NAME    = 'copypasta'
ENABLE  = True
TYPE    = 'command'
PATTERN = re.compile('^!copypasta$')
URL 	= 'https://www.reddit.com/r/copypasta/.json'
MIN_LEN = 0
MAX_LEN = 480

USAGE   = '''Usage: !copypasta
Displays a random post from r/copypasta

WARNING: can be pretty offcolor. Use at your own discretion
'''

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, url=URL):
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    pastas = []
    try:
        for result in json.loads(result.body.decode())['data']['children']:
            data  = result['data']
            pasta = data['selftext'].replace('\n', ' ')

	    # Ignore long posts b/c IRC
            if MIN_LEN < len(pasta) < MAX_LEN:
                pastas.append(pasta)

        response = random.choice(pastas)

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
