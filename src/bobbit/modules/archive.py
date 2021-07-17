# archive.py

import re

from bobbit.utils import shorten_url

# Metadata

NAME    = 'archive'
ENABLE  = True
PATTERN = r'^!archive\s*(?P<url>[^\s]*)$'
USAGE   = '''Usage: !archive <url>
Given a URL, return link to archive.is snapshot of the URL.

If not URL is specified, it will search the channel's history for the previous
URL.

Example:
    > !archive https://waifupaste.moe
    https://yld.me/l1X
'''

# Constants

ARCHIVE_URL = 'https://archive.is/newest/{url}'

# Command

async def archive(bot, message, url=''):
    if not url:
        for m in bot.history.search(message.channel, pattern='http[s]*://', limit=1, reverse= True):
            url = re.findall(r'(http[s]*://[^\s<>]+)', m.body)[0]

    url       = ARCHIVE_URL.format(url=url)
    short_url = await shorten_url(bot.http_client, url)
    response  = bot.client.format_text('{bold}Archive{bold}: {url}', url=short_url)
    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, archive),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
