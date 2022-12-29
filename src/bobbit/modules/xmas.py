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

    # Handle leap year
    if int(now.year+1) % 4 == 0:
        daysleft = delta.days % 366
    else:
        daysleft = delta.days % 365

    # Return response based on number of days left
    if daysleft > 0:
        return message.with_body(f'{daysleft} ' + ('day' if daysleft == 1 else 'days') + ' until Christmas')
    else:
        return message.with_body('0 days left! Merry Christmas!')

# Register

def register(bot):
    return (
        ('command', PATTERN, xmas),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
