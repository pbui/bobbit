# yldme.py

from modules.__common__ import shorten_url

import tornado.gen

# Metadata

NAME    = 'yldme'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!yldme (?P<url>[^\s]*)$'
USAGE   = '''Usage: !yldme <url>
Given a url, return a shortened version.
Example:
    > !yldme https://waifupaste.moe
    https://yld.me/l1X
'''

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, url):
    response = yield shorten_url(url)
    if response != url:
        bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
