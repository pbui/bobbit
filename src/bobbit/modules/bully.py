# bully.py

from random import choice

# Metadata

NAME    = 'bully'
ENABLE  = True
PATTERN = r'^!bully (?P<nick>[^\s]+)'
USAGE   = '''Usage: !bully <nick>
This bullies the user identified by nick.
'''

# Constants

BULLY_PHRASES = [
    '\'s day has been ruined by your message,',
    ' wants to return to monke, but not if you\'re coming, too,',
    ' knows how much of a duck-banging degenerate you are,',
    ' hopes you order pizza from Modern Market, but then you realize you have an interview to go to that you\'re about to be late to, so you frantically rush to it before realizing it\'s over Zoom, so you pull out your laptop and search through your email, but can\'t find the link, before finally discovering it 2 whole minutes later, making you late to your interview, which you fail by the way, after which you remember you ordered pizza which, even though cold, would still be enough to lift your spirits up a little, except you find it was taken by someone else, Modern Market has closed, and you are left with nothing but dread, disgust, and misery,',
    ' believes you\'re too incompetent to know that you\'re being bullied,',
    ' doesn\'t care about your race, sex, or age... or anything about you really,',
    ' has more maidens than you,',
    '\'s faith in society has plummeted since meeting you,',
    ' think you\'re about as good as the dining hall food,',
    ' gives eMoTiOnAL dAmAgE to',
    ' thinks you were probably the pilot of Ever Given when it clogged the Suez Canal,'
]

# Command

async def bully(bot, message, nick):
    if nick not in bot.users:
        return message.with_body(f'Unknown nick: {nick}')
    else:
        return message.with_body(f'{message.nick}{choice(BULLY_PHRASES)} {nick}')

# Register

def register(bot):
    return (
        ('command', PATTERN, bully),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
