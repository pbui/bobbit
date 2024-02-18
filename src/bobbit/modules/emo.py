# emo.py

import random

from bobbit.utils import parse_options

# Metadata

NAME = 'emo'
ENABLE = True
PATTERN = r'!emo\s+(?P<nick>.*)$'
USAGE = '''Usage: !emo [-g -l -a] <nick>
This displays a random emo message sent in the chat with
the following options:

    -g      Grab a new message
    -l      Display the last message that was grabbed
    -a      Display all emo messages
'''

# Command

async def emo(bot, message, nick='pnutzh4x0r'):
    options, nick = parse_options({'-g': False, '-l': False, '-a': False}, nick)
    last_emo = options['-l']
    random_emo = options['-r']
    all_emo = options['-a']
    user = bot.users.get(nick, {})

    # Display Last or Random Emo
    if last_emo or random_emo or all_emo:
        if nick not in bot.users:
            return message.copy(body=f'Unknown nick: {nick}')

        if 'emo' not in user:
            return message.copy(body=f'{nick} is happy, for some reason')

        if last_emo:
            emo = user['emo'][-1]
        elif all_emo:
            return [message.with_body(emo) for emo in user['emo']]
        else:
            emo = random.choice(user['emo'])

        return message.copy(body = emo, nick = nick, highlighted=True)

    if nick not in bot.users:
        bot.users[nick] = {'emo': []}
        user = bot.users[nick]

    for emo in bot.history.search(message.channel, nick=nick, limit=1, reverse=True):
        try:
            user['emo'].append(emo.body)
        except KeyError:
            user['emo'] = [emo.body]

    return message.copy(body = f'Grabbed an emo message from {nick}, cheer up buddy')

# Register

def register(bot):
    return (('command', PATTERN, emo),)
