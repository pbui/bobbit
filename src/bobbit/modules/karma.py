# karma.py

# Metadata

NAME    = 'karma'
ENABLE  = True
PATTERN = r'(?P<nick>[^\s]+)(?P<modifier>[+-]{2})'
USAGE   = '''Usage: nick++ or nick--
This adds or removes karma from specified nick (or word).
Example:
    > ZOMG AndroidKitKat++
    AndroidKitKat now has 69 karma.

    > Hmm sussy--
    sussy now has -420 karma
'''

# TODO: add !karma <nick|word> to display current karma

# Command

async def karma(bot, message, nick, modifier):
    # Prevent users from modifying their own karma
    if nick == message.nick:
        return

    # Compute karma
    dkarma = 1 if modifier == '++' else -1

    if nick in bot.users:   # Nick
        karma = bot.users[nick]['karma'] = bot.users[nick].get('karma', 0) + dkarma
    else:                   # Word (hack using @karam@ user)
        user  = '@karma@'

        if user not in bot.users:
            bot.users[user] = {}

        karma = bot.users[user][nick] = bot.users[user].get(nick, 0) + dkarma

    return message.with_body(
        bot.client.format_text(
            '{bold}' + nick + '{bold} now has {color}' + ('{green}' if karma >= 0 else '{red}') + str(karma) + ' karma {color}'
        )
    )

# Register

def register(bot):
    return (
        ('command', PATTERN, karma),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
