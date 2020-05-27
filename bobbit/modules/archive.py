# archive.py

import logging
import re

# Metadata

NAME    = 'archive'
ENABLE  = False # NOTE: blocked by website
PATTERN = '^!archive (?P<url>[^\s]*)$'
USAGE   = '''Usage: !archive <url>
Given a url, return link to archive.is snapshot.
Example:
    > !archive https://waifupaste.moe
    https://yld.me/l1X
'''

# Constants

ARCHIVE_URL = 'http://archive.vn/search/'
ARCHIVE_RE  = 'href="(http://archive.vn/[^":/*.]+)">'

# Command

async def archive(bot, message, url):
    async with bot.http_client.get(ARCHIVE_URL, params={'q': url}) as response:
        try:
            text     = await response.text()
            response = re.findall(ARCHIVE_RE, text)[0][0]
        except (IndexError, ValueError) as e:
            logging.warning(e)
            response = 'No results'

        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, archive),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
