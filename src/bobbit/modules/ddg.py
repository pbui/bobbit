# ddg.py

import html
import logging
import re

from urllib.parse import unquote
from bobbit.utils import shorten_url, strip_html

# Metadata

NAME    = 'ddg'
ENABLE  = True
PATTERN = '^!ddg (?P<query>.*$)'
USAGE   = '''Usage: !ddg <query>
Given a search query, this returns the first result from DuckDuckGo.
Example:
    > !ddg who likes short shorts?
'''

# Constants

DDG_URL = 'https://duckduckgo.com/html/'
DDG_RE  = '<a.*class="result__a" href=".*ddg=([^"]+)">(.*)</a>'

# Command

async def ddg(bot, message, query=None):
    async with bot.http_client.get(DDG_URL, params={'q': query}) as response:
        try:
            text     = await response.text()
            matches  = re.findall(DDG_RE, text)
            url      = await shorten_url(bot.http_client, unquote(matches[0][0]))
            title    = strip_html(html.unescape(matches[0][1]))
            response = bot.client.format_text(
                '{color}{green}DDG{color}: ' +
                '{bold}{title}{bold} @ {color}{blue}{url}{color}',
                title = title,
                url   = url
            )
        except (IndexError, ValueError) as e:
            logging.warning(e)
            response = 'No results'

        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, ddg),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
