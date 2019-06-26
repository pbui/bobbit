# rms.py
# Made by sbattali

import re

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'rmsporn'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!rmsporn'
USAGE   = '''Usage: !rmsporn
When called, this module responds with a nice image of rms.
Example:
    > !rmsporn
'''

# Constants

RMS_URL = 'http://rms.sexy'

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, album=None):
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, RMS_URL)

    if result.code == 200:
        img_uri = re.search('/img/.*.jpg', str(result.body))
        if img_uri:
            response = RMS_URL + img_uri[0]
            bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
