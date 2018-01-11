# google.py --------------------------------------------------------------------

from modules.__common__ import shorten_url

from urllib.parse import unquote, urlencode

import re

import tornado.httpclient

# Meta-data --------------------------------------------------------------------

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

def command(bot, nick, message, channel, query=None):
    params  = {'q': query}
    url     = GOOGLE_URL + '?' + urlencode(params)
    result  = tornado.httpclient.HTTPClient().fetch(url)
    try:
        url      = unquote(re.findall(b'/url\?q=([^&]*)', result.body)[0].decode())
        response = shorten_url(url)
    except (IndexError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    return bot.format_responses(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
