# xmas.py

import datetime

# Metadata

NAME    = 'xmas'
ENABLE  = True
PATTERN = r'^!xmas\s*$'
USAGE   = '''Usage: !xmas
This prints out the number of days until Christmas.
'''

# Command

async def xmas(bot, message):

    now = datetime.datetime.now()

    delta = datetime.datetime(year=now.year+1, month=12, day=25) - datetime.datetime(year=now.year, month=now.month, day=now.day)

    daysleft = delta.days % 365

    return message.with_body(f'{daysleft} days until Christmas')


# Register

def register(bot):
    return (
        ('command', PATTERN, xmas),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
