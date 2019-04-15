# agency.py

import random

# Metadata

NAME    = 'agency'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<agency>cia|fbi|fiveeyes|kgb|eu|gnu|gnome)$'
USAGE   = '''Usage: !agency
    Will report activity to desired agency
'''

# reasons
reasons = {
        "cia":[
            "This incident has been reported (Case #",
            "This regime will be overthrown (Useless War #"
            ],
        "fbi":[
            "This collusion with Russia has been filed and will be used against you at a politcally opportune moment (Case #"
            ],
        "fiveeyes":[
            "This communication has been intercepted and will be shared among members of the Five Eyes (Case #"
            ],
        "kgb":[
            "The Party has been notified of your bourgeois thought. (Gulag Inmate #"
            ],
        "eu":[
            "Your attempt at executing a mutually beneficial trade has been been brought before the European Commission. (Anti-Trust Case #",
            "Your speech has been regulated. (EU Law #"
            ],
        "gnu":[
            "Your use of proprietary software has been reported to the FSF. (Assigned GNULAG #"
            ],
        "gnome":[
            "Your disgust over KDE has been noted. (Cult Follower #",
            "You are now subscribed to GNOME Facts! (Cult Follower #"
            ]
        }

# Command

def command(bot, nick, message, channel, agency=None):
    report = ''.join(["%s" % random.randint(0, 9) for num in range(0, 5)])
    response = random.choice(reasons[agency]) + report + ")"

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
