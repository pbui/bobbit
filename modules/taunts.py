# taunts.py

import re

# Metadata

NAME    = 'taunts'
ENABLE  = True
TYPE    = 'command'
PATTERN = re.compile('^(?P<taunt>[0-9]+$)')
USAGE   = '''Usage: taunt
Translate taunt number to message (based on Age of Empires II
Example:
    > 1
    Yes
'''

# Constants

# https://steamcommunity.com/sharedfiles/filedetails/?id=711390939

TAUNTS = {
    '1'  : 'Yes',
    '2'  : 'No',
    '7'  : 'Ahh!',
    '8'  : 'All hail, king of the losers!',
    '9'  : 'Ooh!',
    '11' : 'LOL',
    '13' : 'Sure, blame it on your ISP.',
    '14' : 'Start the game already!',
    '17' : 'It is good to be the king.',
    '24' : 'Dadgum.',
    '25' : 'Eh, smite me.',
    '27' : 'You played two hours to die like this?',
    '28' : 'Yeah, well, you should see the other guy.',
    '29' : 'Roggan',
    '30' : 'Wololo',
    '42' : 'What age are you in?',
}

# Command

def command(bot, nick, message, channel, taunt):
    response = TAUNTS.get(taunt, None)
    if response:
        bot.send_message(response, None if channel else nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
