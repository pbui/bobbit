# grab.py

import random

from bobbit.utils import parse_options

# Metadata

NAME    = 'grab'
PATTERN = r'^!grab\s+(?P<nick>.*)$'
ENABLE  = True
USAGE   = '''Usage: !grab [-l -r -a] <nick>
This grabs the last message from nick or it displays previously grabbed
messages with the following options:

    -l      Display the last grabbed message from nick (default).
    -r      Display a random grabbed message from nick.
    -a      Display all grabbed messages from nick (not implemented yet).
'''

# Command

async def grab(bot, message, nick):
    options, nick = parse_options({'-l': False, '-r': False, '-a': False}, nick)
    last_grab     = options['-l']
    random_grab   = options['-r']
    user          = bot.users.get(nick, {})

    # Display Last or Random Grab
    if last_grab or random_grab:
        if nick not in bot.users:
            return message.copy(body=f'Unknown nick: {nick}')

        if 'grabs' not in user:
            return message.copy(body=f'{nick} has no grabs')

        if last_grab:
            grabbed = user['grabs'][-1]
        else:
            grabbed = random.choice(user['grabs'])

        return message.copy(body=grabbed, nick=nick, highlighted=True)

    # Save most recent grab
    if nick not in bot.users:
        bot.users[nick] = {'grabs': []}
        user            = bot.users[nick]

    for grabbed in bot.history.search(message.channel, nick=nick, limit=1, reverse=True):
        try:
            user['grabs'].append(grabbed.body)
        except KeyError:
            user['grabs'] = [grabbed.body]

    return message.copy(body=f'Grabbed last message from {nick}')

# Register

def register(bot):
    return (
        ('command', PATTERN, grab),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
