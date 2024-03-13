# xmas.py

import datetime

# Metadata

NAME    = 'ttb'
ENABLE  = True
PATTERN = r'^!ttb\s*$'
USAGE   = '''Usage: !ttb
This prints out the number of days until pnutz's baby is due.
'''

# Command

async def xmas(bot, message):

    now = datetime.datetime.now()
    delta = datetime.datetime(year=2024, month=10, day=17) - datetime.datetime(year=now.year, month=now.month, day=now.day)

    # Handle leap year
    if int(now.year+1) % 4 == 0:
        daysleft = delta.days % 366
    else:
        daysleft = delta.days % 365

    # Return response based on number of days left
    if daysleft > 0:
        return message.with_body(f'{daysleft} ' + ('day' if daysleft == 1 else 'days') + ' until pnutz\'s baby is due!')
    else:
        return message.with_body('They\'re past due!')

# Register

def register(bot):
    return (
        ('command', PATTERN, xmas),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
