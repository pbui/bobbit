# interject.py -----------------------------------------------------------------

import tornado.gen

# Metadata ---------------------------------------------------------------------

NAME    = 'interject'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!interject (?P<first>[^\s]+) (?P<second>[^\s]+)$'
USAGE   = '''Usage: !ddg <query>
Creates interject meme with first and second arguments.
Example:
    > !interject Linux GNU
    I'd just like to interject for a moment. What you’re referring to as Linux,
    is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus
    Linux. 
'''

# Constants --------------------------------------------------------------------

TEMPLATE = "I'd just like to interject for a moment. What you’re referring to as {first}, is in fact, {second}/{first}, or as I’ve recently taken to calling it, {second} plus {first}."

# Command ----------------------------------------------------------------------

@tornado.gen.coroutine
def command(bot, nick, message, channel, first='Linux', second='GNU'):
    bot.send_response(TEMPLATE.format(first=first, second=second), nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
