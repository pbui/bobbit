# clap.py

# Metadata

NAME    = 'clap'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!clap (?P<phrase>.*)'
USAGE   = '''Usage: !clap <phrase>
Given a phrase, this replaces all spaces with the clap emoji.
Example:
    > !clap Do I look like I'm joking
    Do U0001F44F I U0001F44F look U0001F44F like U0001F44F I'm U0001F44F joking U0001F44F
'''

# Command
def command(bot, nick, message, channel, phrase):
    response = phrase.replace(" ", " \U0001F44F ")
    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
	(PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

