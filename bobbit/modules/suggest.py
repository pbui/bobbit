# suggest.py

import logging

# Metadata

NAME    = 'suggest'
ENABLE  = True
PATTERN = r'^!suggest (?P<target>[-\w#]*) (?P<suggestion>.*)'
USAGE   = '''Usage: !suggest <channel> <message>
This anonymously sends a message to the specified channel.
Example:
    > !suggest #cse-40175-fa18 what about bob?
'''

# Constants

WHITELIST = []
TEMPLATE  = '{color}{red}Anonymous coward suggests{color}: {suggestion}'

# Command

async def suggest(bot, message, target, suggestion):
    if message.highlighted:
        return

    if not target.startswith('#'):
        target = '#' + target

    if not target in WHITELIST:
        return message.with_body(f'Channel {target} not allowed')

    logging.info('Anonymous message from %s: %s', message.nick, message.body)
    return message.copy(
        body    = bot.client.format_text(TEMPLATE, suggestion=suggestion),
        nick    = 'anonymous',
        channel = target,
    )

# Register

def register(bot):
    global WHITELIST, TEMPLATE

    config    = bot.config.load_module_config('suggest')
    WHITELIST = config.get('whitelist', WHITELIST)
    TEMPLATE  = config.get('template' , TEMPLATE)

    return (
        ('command', PATTERN, suggest),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
