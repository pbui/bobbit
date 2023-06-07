# reminders.py

''' Reminder system '''

import collections
import dbm
import json
import time

from bobbit.message import Message
from bobbit.utils   import elapsed_time

# Metadata

NAME    = 'reminders'
ENABLE  = True
PATTERN = r'^!remind\s+(?P<timespec>[^\s]+)\s*(?P<body>.+)$'
USAGE   = '''Usage: !remind timespec reminder
!remind 5h email apple lady
'''
TIMEOUT = 60    # Every minute

# Constants

UNITS = {
    's': 1,
    'm': 60,
    'h': 60*60,
    'd': 24*60*60,
}

# Functions

def parse_timespec(timespec):
    ''' Parse time specification with the following format:

        N[s|m|h|d]

    TODO: Add support for exact time:

        @12:34
    '''
    tokens       = collections.deque(timespec.lower())
    total_time   = 0
    current_time = ''

    while tokens:
        token = tokens.popleft()
        if token.isdigit() or token == '.':
            current_time += token
        else:
            try:
                total_time   += float(current_time) * UNITS.get(token, 0)
                current_time  = ''
            except ValueError:
                return 0

    return total_time

# Command

async def reminders_command(bot, message, timespec, body):
    reminders_path = bot.config.get_config_path('reminders.cache')

    with dbm.open(reminders_path, 'c') as reminders:
        delta = parse_timespec(timespec)
        if not delta:
            return message.with_body(f'Invalid time specification: {timespec}')

        nick = body.split()[0]
        if nick in bot.users:               # XXX: can't use nick as first word in body
            try:
                nick, body = body.split(' ', 1)
            except ValueError:              # XXX: one word body is confused as nick
                nick = message.nick
        else:
            nick = message.nick

        current = time.time()
        timeout = str(current + delta)      # XXX: possible but unlikely collision

        reminders[timeout] = json.dumps({
            'nick': nick,
            'body': body,
            'time': current,
        })

# Timer

async def reminders_timer(bot):
    reminders_path = bot.config.get_config_path('reminders.cache')
    current_time   = time.time()

    with dbm.open(reminders_path, 'c') as reminders:
        for timeout in reminders.keys():
            reminder = json.loads(reminders[timeout])
            elapsed  = elapsed_time(current_time, reminder['time'])
            if float(timeout) < current_time:
                await bot.outgoing.put(Message(
                    nick    = reminder['nick'],
                    channel = None,
                    body    = f'Reminder from {elapsed} ago: {reminder["body"]}',
                    notice  = True,
                ))
                del reminders[timeout]

# Register

def register(bot):
    return (
        ('command', PATTERN, reminders_command),
        ('timer'  , TIMEOUT, reminders_timer),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
