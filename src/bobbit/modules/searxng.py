# searxng.py

import html
import logging

from bobbit.utils import shorten_url

# Metadata

NAME    = 'searxng'
ENABLE  = True
PATTERN = '^!sx (?P<query>.*$)'
USAGE   = '''Usage: !sx <query>
Given a search query, this returns the first result from an SearXNG instance.
Example:
    > !sx who likes short shorts?
'''

# Constants

SEARXNG_URL = 'https://searx.ndlug.org/search'

# Command

async def searxng(bot, message, query=None):
    params = {
        'q'     : query,
        'format': 'json',
    }
    async with bot.http_client.get(SEARXNG_URL, params=params) as response:
        try:
            data  = await response.json()
            item  = data['results'][0]
            title = html.unescape(item['title'])
            url   = await shorten_url(bot.http_client, item['url'])
            response = bot.client.format_text(
                '{color}{green}SearXNG{color}: ' +
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
    global SEARXNG_URL

    config      = bot.config.load_module_config('searxng')
    SEARXNG_URL = config.get('url', SEARXNG_URL)

    return (
        ('command', PATTERN, searxng),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
