# ddg.py -----------------------------------------------------------------------

from modules.__common__ import shorten_url

from urllib.parse import unquote, urlencode

import re

import tornado.gen
import tornado.httpclient

# Metadata ---------------------------------------------------------------------

NAME    = 'ddg'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!ddg (?P<query>.*$)'
USAGE   = '''Usage: !ddg <query>
Given a search query, this returns the first result from DuckDuckGo.
Example:
    > !ddg who likes short shorts?
'''

# Constants --------------------------------------------------------------------

DDG_URL = 'http://duckduckgo.com/html/'
DDG_RX  = '.*result__url.*uddg=([^"]*)">'

# Command ----------------------------------------------------------------------

@tornado.gen.coroutine
def command(bot, nick, message, channel, query=None):
    params = {'q': query, 's': 0}
    url    = DDG_URL + '?' + urlencode(params)
    client = tornado.httpclient.HTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)
    try:
        urls     = [unquote(url)
                        for url in re.findall(DDG_RX, result.body.decode())
                        if 'y.js' not in url]
        response = shorten_url(urls[0])
    except (IndexError, ValueError):
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
