# distrowatch.py
# By: sbattali

from modules.__common__ import shorten_url

from urllib.parse import unquote, urlencode

import re
import random
from textwrap import wrap

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'distrowatch'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!distrowatch (?P<distro>.*$)'
USAGE   = '''Usage: !distrowatch <distro>
Returns a random review of distro from distrowatch
Example:
    > !distrowatch ferenos
'''

# Constants

URL     = 'https://distrowatch.com/dwres.php?resource=ratings&distro={dist}&distribution={dist}&sortby=votes'
MAX_LEN = 420

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, distro):
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, URL.format(dist=distro))

    if result.code == 200:
        # Get only text from table
        quotes   = re.findall(b'\n.*<br /><br /><br /><form name=like method=get>', result.body)
        quotes   = [re.sub('<[^<]+?>', '', str(quote)[2:-1]) for quote in quotes]
        response = re.sub(r'(\\n|\\r)', ' ', random.choice(quotes))
        response = re.sub(r'\\', '', response)

        # Send multiple messages to get the whole review
        responses = [x.strip() for x in wrap(response, width=MAX_LEN)]
        bot.send_response(responses, nick, channel)

# Generator

def get_review(distro):
    return lambda b, n, m, c: command(b, n, m, c, distro)

# Register

def register(bot):
    return (
        (PATTERN, command),
        ('^!FerenOS$', get_review('ferenos')),
        ('^!Solus$'  , get_review('solus')),
        ('^!Fedora$' , get_review('fedora')),
        ('^!Ubuntu$' , get_review('ubuntu')),
        ('^!Arch$'   , get_review('arch')),
        ('^!Void$'   , get_review('void')),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
