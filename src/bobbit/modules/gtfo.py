# gtfo.py

import logging
import time

# Metadata

NAME    = 'gtfo'
PATTERN = r'^@(?P<action>[^@]+)@ (?P<nicks>.*)$'
ENABLE  = True
USAGE   = '''
Monitors idle users and kicks them out.
'''

# Constants

CHANNELS     = []
IDLE_TIMEOUT = 7 * 24 * (60 * 60)   # 1 Week
KICK_TIMEOUT = 5*60                 # Check every 5 minutes

# Command

async def gtfo(bot, message, action, nicks):
    if message.nick != '@IRC@':
        return

    # Update last_seen for users not in bot.users when joining a room or when
    # they join a room
    if action in ('NAMES', 'JOIN'):
        for nick in nicks.split():
            if nick[0] in ('@', '+', '%', '~'):
                nick = nick[1:]

            if nick not in bot.users:
                bot.update_user_seen(nick, message.timestamp)

            bot.update_user_channel(nick, message.channel)

async def kick(bot):
    for nick, user in bot.users.items():
        if nick.startswith('@') or nick == bot.client.nick:
            continue

        last_seen_diff = time.time() - user.get('last_seen', 0.0)
        if last_seen_diff < IDLE_TIMEOUT:
            continue

        for channel in CHANNELS:
            if channel not in user.get('channels', []):
                continue

            logging.info('Kicking %s from %s', nick, channel)
            days = IDLE_TIMEOUT / (24 * 60 * 60)
            await bot.client.send_message(
                f'KICK {channel} {nick} :You have been idle for > {days:0.2f} days'
            )
            # XXX: Remove once we support PART and KICK events
            user['channels'].remove(channel)

# Register

def register(bot):
    global CHANNELS, IDLE_TIMEOUT, KICK_TIMEOUT

    config       = bot.config.load_module_config('gtfo')
    CHANNELS     = config.get('channels', CHANNELS)
    IDLE_TIMEOUT = config.get('idle_timeout' , IDLE_TIMEOUT)
    KICK_TIMEOUT = config.get('kick_timeout' , KICK_TIMEOUT)

    if not config.get('enabled', False):
        return []

    return (
        ('command', PATTERN, gtfo),
        ('timer'  , KICK_TIMEOUT, kick),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
