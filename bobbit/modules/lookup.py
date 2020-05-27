# lookup.py

'''
# Configuration

The lookup module reads from the lookup.yaml file stored in bobbit's
configuration directory.
'''

import logging
import os
import random
import yaml

# Metadata

NAME    = 'lookup'
ENABLE  = True
PATTERN = '^!(?P<query>.*)'
USAGE   = '''Usage: !<query> [-a]
This looks up the given query (-a displays all matches).
Example:
    > !whois pbui
    Worst professor ever!
'''

# Constants

LOOKUP_PATH = None
LOOKUP_DATA = {}
LOOKUP_TIME = None

# Lookup

def lookup_data():
    global LOOKUP_TIME, LOOKUP_DATA

    mtime = os.path.getmtime(LOOKUP_PATH)
    if LOOKUP_TIME is None or LOOKUP_TIME < mtime:
        LOOKUP_DATA = yaml.safe_load(open(LOOKUP_PATH, 'rb'))
        LOOKUP_TIME = mtime

    return LOOKUP_DATA

def lookup_r(key, data=None):
    # TODO: Document (there be dragons here)
    data   = data or lookup_data()
    result = data.get(key, None)
    args   = '__default__'
    if not result:
        key, args = key.split(' ', 1)
        result    = data.get(key, None)

    if isinstance(result, str):
        if result.startswith('!'):
            if args.split()[-1] == '-a':
                return lookup_r(result[1:] + ' -a')
            else:
                return lookup_r(result[1:])
        return result.split('\n')
    elif isinstance(result, list):
        if args.split()[-1] == '-a':
            return result
        return [random.choice(result)]
    elif isinstance(result, dict):
        return lookup_r(args, result) or lookup_r('__default__', result)
    else:
        return None

# Command

async def lookup(bot, message, query=None):
    try:
        responses = lookup_r(query.strip().lower())
        if responses:
            return [message.with_body(r) for r in responses]
    except (IOError, ValueError):
        return None

# Register

def register(bot):
    global LOOKUP_PATH, LOOKUP_DATA

    try:
        LOOKUP_PATH = os.path.join(bot.config.config_dir, 'lookup.yaml')
        LOOKUP_DATA = lookup_data()
    except (IOError, OSError) as e:
        logging.warning(e)
        return []

    return (
        ('command', PATTERN, lookup),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
