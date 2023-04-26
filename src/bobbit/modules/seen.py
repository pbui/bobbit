# seen.py

import time

from bobbit.utils import elapsed_time

# Metadata

NAME    = 'seen'
PATTERN = r'^!seen\s*(?P<nick>[^\s]*)$'
ENABLE  = True
USAGE   = '''Usage: !seen <nick>
This reports the last time a user was seen (ie. last time they sent a
message).
'''

# Command

async def seen(bot, message, nick):
    current_time = time.time()

    # Handle single specific user
    if nick:
        if nick not in bot.users:
            return message.with_body(f'Unknown user: {nick}')

        last_seen = bot.users[nick].get('last_seen')
        if not last_seen:
            return message.with_body(f'{nick} has not been seen yet')

        return message.with_body(
            f'{nick} was last seen {elapsed_time(current_time, last_seen)} ago'
        )

    # Handle all users
    users = [nick for nick in bot.users if 'last_seen' in bot.users[nick] and message.channel in bot.users[nick].get('channels', [])]
    nicks = sorted(users, key=lambda nick: bot.users[nick]['last_seen'])[:5]
    return [
        message.with_body(f'{nick} was last seen {elapsed_time(current_time, bot.users[nick]["last_seen"])} ago') for nick in nicks
    ]

# Register

def register(bot):
    return (
        ('command', PATTERN, seen),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
