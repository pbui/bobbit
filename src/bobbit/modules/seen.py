# seen.py

import time

# Metadata

NAME    = 'seen'
PATTERN = r'^!seen\s+(?P<nick>.*)$'
ENABLE  = True
USAGE   = '''Usage: !seen <nick>
This reports the last time a user was seen (ie. last time they sent a
message).
'''

# Functions

def elapsed_time(s):
    elapsed = time.time() - s
    units   = (
        ('seconds', 60),
        ('minutes', 60),
        ('hours'  , 24),
        ('days'   , 7),
        ('weeks'  , 52),
    )
    for unit, step in units:
        if elapsed < step:
            break
        elapsed /= step

    return '{:0.2f} {} ago'.format(elapsed, unit)

# Command

async def seen(bot, message, nick):
    if nick not in bot.users:
        return message.with_body(f'Unknown nick: {nick}')

    last_seen = bot.users[nick].get('last_seen')
    if not last_seen:
        return message.with_body(f'{nick} has not been seen yet')

    return message.with_body(f'{nick} was last seen {elapsed_time(last_seen)}')

# Register

def register(bot):
    return (
        ('command', PATTERN, seen),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
