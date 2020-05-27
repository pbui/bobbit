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

LOOKUP_DATA = {}
LOOKUP_PATH = None
LOOKUP_TIME = 0

# Lookup

def lookup_data():
    global LOOKUP_TIME, LOOKUP_DATA

    mtime = os.path.getmtime(LOOKUP_PATH)
    if not LOOKUP_TIME or LOOKUP_TIME < mtime:
        try:
            LOOKUP_DATA = yaml.safe_load(open(LOOKUP_PATH))
            LOOKUP_TIME = mtime
        except (IOError, OSError, yaml.parser.ParserError) as e:
            logging.warning('Unable to parse lookup data: %s', e)

    return LOOKUP_DATA

def lookup_r(key, data=None):
    data   = data or lookup_data()  # Use given directory or use global dictionary
    result = data.get(key, None)
    args   = '__default__'
    if not result:
        key, args = key.split(' ', 1)
        result    = data.get(key, None)

    # Result is a string, so recursive if it is an alias, otherwise return all
    # of by spliting by newlines.
    if isinstance(result, str):
        if result.startswith('!'):
            if args.split()[-1] == '-a':
                return lookup_r(result[1:] + ' -a')
            else:
                return lookup_r(result[1:])
        return result.split('\n')

    # Result is a list, so either turn all of it or pick one at random.
    elif isinstance(result, list):
        if args.split()[-1] == '-a':
            return result
        return [random.choice(result)]

    # Result is a dictionary, so recurse on the remaining arguments with this
    # dictionary or the default entry.
    elif isinstance(result, dict):
        return lookup_r(args, result) or lookup_r('__default__', result)

    # Nothing matches, so return None.
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
    global LOOKUP_PATH

    LOOKUP_PATH = bot.config.get_config_path('lookup.yaml')
    return (
        ('command', PATTERN, lookup),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
