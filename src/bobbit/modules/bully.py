# bully.py

from random import choice

# Metadata

NAME = 'bully'
ENABLE = True
PATTERN = r'^!bully (?P<nick>)$'
USAGE = '''Usage: !bully <nick>
This bullies the user identified by nick.
'''

# Constants

# feel free to add to these...
BULLY_PHRASES = [
    '\'s day has been ruined by your message,',
    ' thinks that your message is the worst thing that they have ever seen and wishes that you have never even thought of it,',
    ' thinks that your brain may be even smoother than your average r/WSBer,',
    ' wants to return to monke, but not if you\'re coming, too,',
    ' thinks you were probably the pilot of Ever Given when it clogged the Suez Canal,'
]

# Command

async def bully(bot, message, nick):
    if nick not in bot.users:
        return message.with_body(f'Unknown nick: {nick}')
    # tell the user how bad their message was
    else:
        return message.with_body(f'{message.nick}{choice(BULLY_PHRASES)} {nick}')

# Register

def register(bot):
    return (
        ('command', PATTERN, bully),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
