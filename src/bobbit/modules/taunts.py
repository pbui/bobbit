# taunts.py

# Metadata

NAME    = 'taunts'
ENABLE  = True
PATTERN = '^(?P<taunt>[0-9]+$)'
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
    '3'  : 'Food please',
    '4'  : 'Wood please',
    '5'  : 'Gold please',
    '6'  : 'Stone please',
    '7'  : 'Ahh!',
    '8'  : 'All hail, king of the losers!',
    '9'  : 'Ooh!',
    '10' : "I'll beat you back to Age of Empires.",
    '11' : 'LOL',
    '12' : 'AGH, He rushed.',
    '13' : 'Sure, blame it on your ISP.',
    '14' : 'Start the game already!',
    '15' : "Don't point that thing at me!",
    '16' : 'Enemy sighted!',
    '17' : 'It is good to be the king.',
    '18' : 'Monk! I need a monk!',
    '19' : 'Long time, no siege.',
    '20' : 'My granny could scrap better than that.',
    '21' : "Nice town, I'll take it",
    '22' : 'Quit touching me!',
    '23' : 'Raiding party!',
    '24' : 'Dadgum.',
    '25' : 'Eh, smite me.',
    '26' : 'The wonder, the wonder, the... no!',
    '27' : 'You played two hours to die like this?',
    '28' : 'Yeah, well, you should see the other guy.',
    '29' : 'Roggan',
    '30' : 'Wololo',
    '31' : 'Attack an enemy now.',
    '32' : 'Cease creating extra villagers.',
    '33' : 'Create extra villagers.',
    '34' : 'Build a navy.',
    '35' : 'Stop building a navy.',
    '36' : 'Wait for my signal to attack.',
    '37' : 'Build a wonder.',
    '38' : 'Give me your extra resources.',
    '42' : 'What age are you in?',
}

# Command

async def command(bot, message, taunt):
    response = TAUNTS.get(taunt, None)
    if response:
        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
