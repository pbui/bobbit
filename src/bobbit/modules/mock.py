# mock.py

# Metadata

NAME    = 'mock'
ENABLE  = True
PATTERN = r'^!mock (?P<phrase>.*)'
USAGE   = '''Usage: !mock <phrase|nick>
Given a phrase, this translates the phrase into a mocking spongebob phrase.
Example:
    > !mock it should work on slack and irc
    iT ShOuLd wOrK On sLaCk aNd iRc

Alternatively, given a nick, this translates the last message from the user
into a mocking spongebob phrase.
Example:
    > !mock AndroidKitKat
    I LoVe aPpLe
'''

# Command

async def mock(bot, message, phrase):
    if phrase in bot.users:
        try:
            history = bot.history.search(message.channel, nick=phrase, limit=1, reverse=True)
            phrase  = list(history)[0].body
        except IndexError:
            pass

    phrase   = phrase.lower().rstrip()
    response = ''

    for count, letter in enumerate(phrase):
        if count % 2:
            letter = letter.upper()
        response += letter

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, mock),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
