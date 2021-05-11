# irc.py

# Metadata

NAME    = 'irc'
PATTERN = r'^@(?P<action>[^@]+)@ (?P<nicks>.*)$'
ENABLE  = True
USAGE   = '''
Dirty hack for IRC events (because protocol objects don't have a reference to
bot object).
'''

# Command

async def irc(bot, message, action, nicks):
    if message.nick != '@IRC@':
        return

    if action in ('NAMES', 'JOIN'):
        # Update last_seen and channel for users when bot joins a room or when
        # a user joins a room
        for nick in nicks.split():
            if nick[0] in ('@', '+', '%', '~'):
                nick = nick[1:]

            # Update last_seen if this is the first time seeing the user or if
            # this is a JOIN action
            if nick not in bot.users or action == 'JOIN':
                bot.update_user_seen(nick, message.timestamp)

            # Always update channel
            bot.update_user_channel(nick, message.channel)
    elif action in ('KICK', 'PART'):
        # Remove users from channel on part or kick
        for nick in nicks.split():
            bot.remove_user_channel(nick, message.channel)
    elif action == 'QUIT':
        # Remove channels from user data
        for nick in nicks.split():
            for channel in bot.users.get(nick, {}).get('channels', []):
                bot.remove_user_channel(nick, channel)
    elif action == 'NICK':
        # Handle NICK change
        old_nick, new_nick  = nicks.split()
        if old_nick in bot.users:
            bot.users[new_nick] = bot.users.pop(old_nick)
        else:
            bot.users[new_nick] = {}

# Register

def register(bot):
    config = bot.config.load_module_config('irc')

    if not config.get('enabled', False):
        return []

    return (
        ('command', PATTERN, irc),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
