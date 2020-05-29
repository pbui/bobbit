# mock.py

# Metadata

NAME    = 'mock'
ENABLE  = True
PATTERN = r'^!mock (?P<phrase>.*)'
USAGE   = '''Usage: !mock <phrase>
Given a phrase, this translates the phrase into a mocking spongebob phrase.
Example:
    > !mock it should work on slack and irc
    iT ShOuLd wOrK On sLaCk aNd iRc
'''

# Command

async def mock(bot, message, phrase):
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
