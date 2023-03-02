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
    ' has a confession to make. You\'re ugly,',
    ' thinks you\'re so ugly that when your mom dropped you off at school she got a fine for littering, ',
    ' thinks your brain is so tiny that you\'d have to stand on a penny to see over it, ',
    ' thinks that you must have been born on a highway, since that\'s where most accidents happen, ',
    ' heard that you\'re so dumb, you thought a quarterback was a refund, ',
    ' would like to see things from your point of view, but can\'t seem to get their head that far up your butt, ',
    ' thinks that your family tree must be a cactus because everyone on it is a prick, ',
    ' thinks that if laughter is the best medicine, your face must be curing the world, ',
    ' thinks that you\'re so ugly, you scared the crap out of the toilet, ',
    ' isn\'t saying you\'re stupid, they\'re just saying you\'ve got bad luck when it comes to thinking, ',
    ' heard you got a brain transplant and the brain rejected you, ',
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
