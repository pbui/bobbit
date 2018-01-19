# suggest.py -------------------------------------------------------------------

# Metadata ---------------------------------------------------------------------

NAME    = 'suggest'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!suggest (?P<target>[-\w]*) (?P<suggestion>.*)'
USAGE   = '''Usage: !suggest <channel> <message>
This anonymously sends a message to the specified channel.
Example:
    > !suggest cse-40175-sp18 what about bob?
'''

# Constants --------------------------------------------------------------------

CHANNELS = ('cse-40175-sp18',)

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, target, suggestion):
    if target in CHANNELS:
        bot.logger.info('Anonymous message from %s: %s', nick, message)
        bot.send_response(suggestion, 'anonymous', '#' + target)
    else:
        bot.send_response('Channel {} not allowed'.format(target), nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
