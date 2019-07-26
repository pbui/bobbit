# aliases.py

'''
# Configuration

Store aliases in aliases.yaml file in bobbit configuration directory:

    aliases:
        # Distrowatch aliases
        Arch:     '!distrowatch arch'
        Fedora:   '!distrowatch fedora'
        FerenOS:  '!distrowatch ferenos'
        Solus:    '!distrowatch solus'
        Ubuntu:   '!distrowatch ubuntu'
        Void:     '!distrowatch void'

        # Google aliases
        so:       '!g site:stackoverflow.com'
        nd:       '!g site:nd.edu'

        # Reddit aliases
        riseup:   '!reddit gamersriseup'
'''

import os
import yaml

# Metadata

NAME    = 'alias'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<alias>[^ ]+)\s*(?P<arguments>.*)'
USAGE   = '''Usage: !alias
'''

# Constants

ALIASES = {}

# Command

def command(bot, nick, message, channel, alias=None, arguments=None):
    try:
        message = '{} {}'.format(ALIASES[alias], arguments or '').rstrip()
    except KeyError:
        return

    bot.process_command(nick, message, channel)

# Register

def register(bot):
    global ALIASES

    try:
        aliases_path = os.path.join(bot.config_dir, 'aliases.yaml')
        aliases_data = yaml.load(open(aliases_path))
        ALIASES      = aliases_data.get('aliases', {})
    except (KeyError, IOError):
        pass

    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
