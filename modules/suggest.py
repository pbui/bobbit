# suggest.py

import random

# Metadata

NAME    = 'suggest'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!suggest (?P<target>[-\w#]*) (?P<suggestion>.*)'
USAGE   = '''Usage: !suggest <channel> <message>
This anonymously sends a message to the specified channel.
Example:
    > !suggest #cse-40175-fa18 what about bob?
'''

# Constants

CHANNELS = ('csememes', 'gaming', 'ndlug')
#NICKS    = ('pbui', 'U0HK21CP2', 'U6R5KVD4L', 'UF7RAN95W')

REJECTS  = (
    "You better check yourself before you wreck yourself",
    "Doesn't look like anything to me",
    "I'm sorry, I'm afraid I can't do that",
    "Channel {channel} not allowed",
    "You shall not pass!",
    "I'll be reporting this to MD",
    "RAMZI SAYS NO SUDO",
)

# Command

def command(bot, nick, message, channel, target, suggestion):
    target = target[1:] if target.startswith('#') else target
    if target in CHANNELS and nick in bot.verified:
        bot.logger.info('Anonymous message from %s: %s', nick, message)
        bot.send_response('Anonymous coward suggests: ' + suggestion, 'anonymous', '#' + target)
    else:
        bot.send_response(random.choice(REJECTS).format(channel=target), nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
