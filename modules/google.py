# google.py --------------------------------------------------------------------

from modules.__common__ import shorten_url

from urllib.parse import unquote, urlencode

import re

import tornado.gen
import tornado.httpclient

# Metadata ---------------------------------------------------------------------

NAME    = 'google'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!g (?P<query>.*$)'
USAGE   = '''Usage:  !g <query>
Given a search query, this returns the first result from Google
Example:
    > !g who likes short shorts?
'''

# Constants --------------------------------------------------------------------

GOOGLE_URL = 'http://www.google.com/search'

# Command ----------------------------------------------------------------------

@tornado.gen.coroutine
def command(bot, nick, message, channel, query=None):
    params = {'q': query}
    url    = GOOGLE_URL + '?' + urlencode(params)
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    try:
        urls     = re.findall(b'/url\?q=([^&]*)', result.body)
        response = shorten_url(unquote(urls[0].decode()))
    except (IndexError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
