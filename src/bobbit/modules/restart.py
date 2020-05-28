# restart.py

import logging
import random

# Metadata

NAME    = 'restart'
ENABLE  = True
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

# Command

async def reload(bot, message):
    if message.highlighted or message.nick not in bot.config.owners:
        return

    logging.info('Reload initiated by %s', message.nick)
    bot.reload()
    return message.with_body(random.choice(RELOAD_MESSAGES))

async def restart(bot, message):
    if message.highlighted or message.nick not in bot.config.owners:
        return

    logging.info('Restart initiated by %s', message.nick)
    bot.restart()

# Register

def register(bot):
    return (
        ('command', '^!restart$', restart),
        ('command', '^!reload$' , reload),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
