import random
import re

# Meta-data --------------------------------------------------------------------

NAME    = '8ball'
ENABLE  = True
TYPE    = 'command'
PATTERN = re.compile('^!8ball (?P<question>.*)')
USAGE   = ''' 8ball Module
Usage:  !8ball <question>

Given a question, this module responds with a magic 8-ball prediction.

Example:

        > !8ball Will pbui ever get tenure at Notre Dame?
        Don't count on it
'''

# Constants --------------------------------------------------------------------

RESPONSES = (
    (   # Affirmative
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes -- definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
    ),
    (   # Maybe
        'Reply hazy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
    ),
    (   # Negative
        'Dont count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful',
        'NOOOOO WAY',
    )
)

# Command -----------------------------------------------------------------------

def command(bot, nick, message, channel, question=None):
    response = random.choice(random.choice(RESPONSES))
    return bot.format_responses(response, nick, channel)

# Register ----------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
