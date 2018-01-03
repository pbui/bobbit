# ddg.py -----------------------------------------------------------------------

from modules.__common__ import shorten_url

from urllib.parse import unquote, urlencode

import re
import tornado.httpclient

# Meta-data --------------------------------------------------------------------

NAME    = 'ddg'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!ddg (?P<query>.*$)'
USAGE   = '''Usage:  !ddg <query>
Given a search query, this returns the first result from DuckDuckGo.
Example:
    > !ddg who likes short shorts?
'''

# Constants --------------------------------------------------------------------

DDG_URL = 'http://duckduckgo.com/html/'
DDG_RX  = '.*result__url.*uddg=([^"]*)">'

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, query=None):
    params  = {'q': query, 's': 0}
    url     = DDG_URL + '?' + urlencode(params)
    result  = tornado.httpclient.HTTPClient().fetch(url)
    try:
        urls     = [unquote(url)
                        for url in re.findall(DDG_RX, result.body.decode())
                        if 'y.js' not in url]
        response = shorten_url(urls[0])
    except (IndexError, ValueError):
        response = 'No results'

    return bot.format_responses(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
