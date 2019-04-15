# mock.py

# Metadata

NAME    = 'mock'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!mock (?P<phrase>.*)'
USAGE   = '''Usage: !mock <phrase>
Given a phrase, this translates the phrase into a mocking spongebob phrase.
Example:
    > !mock it should work for slack and irc
      iT ShOuLd wOrK On sLaCk aNd iRc      
'''

# Constants

# Command

def command(bot, nick, message, channel, phrase):
    phrase = phrase.lower().rstrip()
    response = "" 

    for count, letter in enumerate(phrase):
        if count % 2: letter = letter.upper()
        response+=letter    

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

