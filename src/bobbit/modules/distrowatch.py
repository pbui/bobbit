# distrowatch.py

import re
import random

from bobbit.utils import strip_html

# Metadata

NAME    = 'distrowatch'
ENABLE  = True
PATTERN = '^!distrowatch (?P<distro>.*$)'
USAGE   = '''Usage: !distrowatch <distro>
Returns a random review of distro from distrowatch
Example:
    > !distrowatch ferenos
'''

# Constants

DW_URL      = 'https://distrowatch.com/dwres.php'
DW_RE       = r'\n(.*)<br /><br /><br /><form name=like method=get>'

# Command

async def command(bot, message, distro):
    params = {
        'resource': 'ratings',
        'distro'  : distro,
        'sortby'  : 'votes',
    }
    async with bot.http_client.get(DW_URL, params=params) as response:
        # Get only text from table
        text     = await response.text()
        quotes   = [strip_html(q) for q in re.findall(DW_RE, text)]
        response = random.choice(quotes)

        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
