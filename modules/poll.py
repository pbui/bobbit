# poll.py

import collections

# Metadata

NAME    = 'poll'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!poll (?P<command>.*)'
COUNTRX = '^(?P<number>[0-9])$'
USAGE   = '''Usage: !poll <command>
This starts and stops a poll and displays a tally.
Example:
    > !poll start

    > !poll stop
    Results: 1 (50%) 2 (50%)
'''

# Globals

PollData  = collections.defaultdict(int)
PollNicks = set()

# Command

def command(bot, nick, message, channel, command=None):
    if nick != bot.owner:
        return

    global PollData
    global PollNicks
    if command == 'start':
        PollData  = collections.defaultdict(int)
        PollNicks = set()

        response = 'Starting poll...'
        bot.send_message(response, channel=channel)
        bot.suppress_taunts = True
    elif command == 'stop':
        n = sum(PollData.values())
        d = ['{} ({:0.2f}%)'.format(k, v *100.0/ n) for k,v in PollData.items()]
        response = 'Results: ' + ', '.join(d)
        bot.send_message(response, channel=channel)
        bot.suppress_taunts = False

def count(bot, nick, message, channel, number=None):
    if not number or nick in PollNicks:
        return

    PollData[number] += 1
    PollNicks.add(nick)

# Register

def register(bot):
    return (
        (PATTERN, command),
        (COUNTRX, count),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
