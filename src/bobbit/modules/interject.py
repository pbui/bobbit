# interject.py

# Metadata

NAME    = 'interject'
ENABLE  = True
PATTERN = r'^!interject (?P<first>(".+")|([^\s]+)) (?P<second>(".+")|([^\s]+))$'
USAGE   = '''Usage: !interject <first> <second>
Creates interject meme with first and second arguments.
Example:
    > !interject Linux GNU
    I'd just like to interject for a moment. What you’re referring to as Linux,
    is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus
    Linux. 
'''

# Constants

TEMPLATE = "I'd just like to interject for a moment. What you’re referring to as {first}, is in fact, {second}/{first}, or as I’ve recently taken to calling it, {second} plus {first}."

# Command

async def interject(bot, message, first='Linux', second='GNU'):
    if first[0] == '"' and first[-1] == '"':
      first = first[1:-1]

    if second[0] == '"' and second[-1] == '"':
      second = second[1:-1]

    return message.with_body(TEMPLATE.format(first=first, second=second))

# Register

def register(bot):
    return (
        ('command', PATTERN, interject),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
