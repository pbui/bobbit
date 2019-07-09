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
    if nick not in bot.owners:
        return

    try:
        command, question = command.split(' ', 1)
    except ValueError:
        pass

    if command in ('start', 'open', 'begin'):
        bot.poll_votes[channel] = {}

        response = 'Starting poll: {}'.format(question)
        bot.send_message(response, channel=channel)
        bot.suppress_taunts.add(channel)
    elif command in ('stop', 'close', 'end'):
        c = collections.Counter(bot.poll_votes[channel].values())
        s = sum(c.values())
        d = ['{} ({}: {:0.2f}%)'.format(k, v, v *100.0/ s) for k,v in sorted(c.items())]
        response = 'Results: ' + ', '.join(d)
        bot.send_message(response, channel=channel)
        bot.suppress_taunts.remove(channel)

def count(bot, nick, message, channel, number=None):
    bot.poll_votes[channel][nick] = int(number)

# Register

def register(bot):
    bot.poll_votes = collections.defaultdict(dict)
    return (
        (PATTERN, command),
        (COUNTRX, count),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
