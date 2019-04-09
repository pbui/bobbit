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
URL = 'https://www.reddit.com/r/copypasta/.json'

USAGE   = '''Usage: !copypasta
Displays a random post from r/copypasta\n
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
            pasta = data['selftext']

			# ignore long posts b/c irc
            if(len(pasta) > 120):
                continue
            pastas.append(pasta)

        response = random.choice(pastas)

    except (IndexError, KeyError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    bot.send_response(response, None if channel else nick, channel)

# Register

def register(bot):
    bot.suppress_taunts = set()
    return (
        (PATTERN, command),
    )
# vim: set sts=4 sw=4 ts=8 expandtab ft=python: