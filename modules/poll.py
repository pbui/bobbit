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
    > !poll start question...
    Poll: question...

    > !poll stop
    Results: 1 (50%) 2 (50%)
'''

# Command

def command(bot, nick, message, channel, command=None):
    if nick != bot.owner:
        return

    try:
        command, question = command.split(' ', 1)
    except ValueError:
        pass

    if command in ('start', 'open', 'begin'):
        bot.poll_votes = {}

        response = 'Starting poll: {}'.format(question)
        bot.send_message(response, channel=channel)
        bot.suppress_taunts = True
    elif command in ('stop', 'close', 'end'):
        c = collections.Counter(bot.poll_votes.values())
        d = ['{} ({}: {:0.2f}%)'.format(k, v, v *100.0/ len(c)) for k,v in sorted(c.items())]
        response = 'Results: ' + ', '.join(d)
        bot.send_message(response, channel=channel)
        bot.suppress_taunts = False

def count(bot, nick, message, channel, number=None):
    bot.poll_votes[nick] = number

# Register

def register(bot):
    bot.poll_votes = {}
    return (
        (PATTERN, command),
        (COUNTRX, count),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
