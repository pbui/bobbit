import os
import random
import re
import sys
import time

# Meta-data --------------------------------------------------------------------

NAME    = 'restart'
ENABLE  = True
TYPE    = 'command'
USAGE   = ''' restart Module
Usages: !restart    # Restarts the bot process
        !reload     # Reloads the bot modules

Examples:

        > !restart

        > !reload
'''

# Constants ---------------------------------------------------------------------

RELOAD_MESSAGES = (
    "I'm... back!",
    'Locked and loaded!',
    'Harder, Better, Faster, Stronger!',
)

RESTART_TIMEOUT = 5

# Command -----------------------------------------------------------------------

def reload_command(bot, nick, message, channel, question=None):
    if nick != bot.owner:
        return None

    bot.logger.debug('Reload initiated by %s', nick)
    bot.load_modules()
    return bot.format_responses(random.choice(RELOAD_MESSAGES), nick, channel)

def restart_command(bot, nick, message, channel, question=None):
    if nick != bot.owner:
        return None

    bot.logger.debug('Restart initiated by %s', nick)
    bot.tcp_stream.close()
    time.sleep(RESTART_TIMEOUT)
    os.execvp(sys.argv[0], sys.argv)

# Register ----------------------------------------------------------------------

def register(bot):
    return (
        (re.compile('^!restart$'), restart_command),
        (re.compile('^!reload$') , reload_command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
