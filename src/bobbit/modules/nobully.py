# nobully.py

# Metadata

NAME = 'nobully'
ENABLE = True
PATTERN = r'^!nobully (?P<nick>)$'
USAGE = '''Usage: !nobully <nick>
This informs the user identified by nick that they should no longer bully other (innocent) users.
'''

# Constants

NOBULLY_URL = 'https://www.stop-irc-bullying.info/'

# Command

async def nobully(bot, message, nick):
    if nick not in bot.users:
        return message.with_body(f'Unknown nick: {nick}')
    # tell the targeted user to stop bullying other users
    else:
        return message.with_body(f'{message.nick} thinks that you should stop bullying other users, {nick}. Please refer to {NOBULLY_URL} for more information.')

# Register

def register(bot):
    return (
        ('command', PATTERN, nobully),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
