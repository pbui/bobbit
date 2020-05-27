# suggest.py

import logging
import os
import yaml

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

    target = target[1:] if target.startswith('#') else target
    if not target in WHITELIST:
        return message.with_body(f'Channel #{target} not allowed')

    logging.info('Anonymous message from %s: %s', message.nick, message.body)
    return message.copy(
        body    = bot.client.format_text(TEMPLATE, suggestion=suggestion),
        nick    = 'anonymous',
        channel = '#' + target,
    )

# Register

def register(bot):
    global WHITELIST, TEMPLATE

    config_path = os.path.join(bot.config.config_dir, 'suggest.yaml')
    try:
        config    = yaml.safe_load(open(config_path))
        WHITELIST = config.get('whitelist', WHITELIST)
        TEMPLATE  = config.get('template' , TEMPLATE)
    except (IOError, KeyError) as e:
        logging.warning(e)
        return []

    return (
        ('command', PATTERN, suggest),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
