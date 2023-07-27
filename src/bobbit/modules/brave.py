# brave.py

import html
import json
import logging
import re

from bobbit.utils import shorten_url, strip_html

# Metadata

NAME    = 'brave'
ENABLE  = True
PATTERN = '^!brave (?P<query>.*$)'
USAGE   = '''Usage: !brave <query>
Given a search query, this returns the first result from Brave.
Example:
    > !brave who likes short shorts?
'''

# Constants

BRAVE_URL = 'https://search.brave.com/search'
BRAVE_RE  = r'data="(.*score.*)"'

# Command

async def brave(bot, message, query=None):
    async with bot.http_client.get(BRAVE_URL, params={'q': query}) as response:
        try:
            text = await response.text()

            for result in re.findall(BRAVE_RE, text):
                data = json.loads(html.unescape(result))

                if 'search' in data:
                    data = data['search']['web']['results'][0]
                elif 'results' in data:
                    data = data['results'][0]
                else:
                    continue

                url      = await shorten_url(bot.http_client, data['url'])
                title    = strip_html(html.unescape(data['title']))
                response = bot.client.format_text(
                    '{color}{green}Brave{color}: ' +
                    '{bold}{title}{bold} @ {color}{blue}{url}{color}',
                    title = title,
                    url   = url
                )
                break
        except (IndexError, ValueError) as e:
            logging.warning(e)
            response = 'No results'

        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, brave),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
