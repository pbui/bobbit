# restart.py

import os
import random
import sys
import time

# Metadata

NAME    = 'restart'
ENABLE  = True
TYPE    = 'command'
USAGE   = '''Usage: [!restart | !reload]
Given one of these two commands, the bot will either restart the entire process
or reload the bot modules.
'''

# Constants

RELOAD_MESSAGES = (
    "I'm... back!",
    'Locked and loaded!',
    'Harder, Better, Faster, Stronger!',
)

RESTART_TIMEOUT = 5

# Command

def reload_command(bot, nick, message, channel, question=None):
    if nick != bot.owner:
        return

    bot.logger.debug('Reload initiated by %s', nick)
    bot.load_modules()
    bot.send_response(random.choice(RELOAD_MESSAGES), nick, channel)

def restart_command(bot, nick, message, channel, question=None):
    if nick != bot.owner:
        return

    bot.logger.debug('Restart initiated by %s', nick)
    bot.tcp_stream.close()
    time.sleep(RESTART_TIMEOUT)
    os.execvp(sys.argv[0], sys.argv)

# Register

def register(bot):
    return (
        ('^!restart$', restart_command),
        ('^!reload$' , reload_command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
