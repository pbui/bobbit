# echo.py

# Metadata

NAME    = 'echo'
ENABLE  = True
PATTERN = r'^!echo\s+(?P<phrase>.*)$'
USAGE   = '''Usage: !echo phrase
This repeats the phrase back to the sender.
'''

# Command

async def echo(bot, message, phrase):
    return message.with_body(phrase)

# Register

def register(bot):
    return (
        ('command', PATTERN, echo),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
