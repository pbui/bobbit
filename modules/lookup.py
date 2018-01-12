# lookup.py -------------------------------------------------------------------

'''
Configuration
=============

The lookup module reads from the lookup.yaml file stored in bobbit's working
directory.
'''

import os
import random
import yaml

# Metadata ---------------------------------------------------------------------

NAME    = 'lookup'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<query>.*)'
USAGE   = '''Usage: !<query> [-a]
This looks up the given query (-a displays all matches).
Example:
    > !whois pbui
    Worst professor ever!
'''

# Constants --------------------------------------------------------------------

LOOKUP_PATH = None
LOOKUP_DATA = {}
LOOKUP_TIME = None

# Lookup -----------------------------------------------------------------------

def lookup_data(path=None):
    global LOOKUP_TIME, LOOKUP_DATA

    mtime = os.path.getmtime(LOOKUP_PATH)
    if LOOKUP_TIME is None or LOOKUP_TIME < mtime:
        LOOKUP_DATA = yaml.load(open(LOOKUP_PATH))
        LOOKUP_TIME = mtime

    return LOOKUP_DATA

def lookup(key, data=None):
    data   = data or lookup_data()
    result = data.get(key, None)
    args   = '__default__'
    if not result:
        key, args = key.split(' ', 1)
        result    = data.get(key, None)

    if isinstance(result, str):
        if result.startswith('!'):
            return lookup(result[1:])
        return result.split('\n')
    elif isinstance(result, list):
        if args.split()[-1] == '-a':
            return result
        return random.choice(result)
    elif isinstance(result, dict):
        return lookup(args, result) or lookup('__default__', result)
    else:
        return []

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, query=None):
    try:
        response = lookup(query)
    except (IOError, ValueError) as e:
        bot.logger.warn(e)
        return

    bot.send_response(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    global LOOKUP_PATH

    LOOKUP_PATH = os.path.join(bot.config_dir, 'lookup.yaml')
    LOOKUP_DATA = lookup_data()

    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
