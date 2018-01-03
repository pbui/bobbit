# help.py -----------------------------------------------------------------------

import random

# Meta-data ---------------------------------------------------------------------

NAME    = 'help'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!help (?P<module_name>.*)'
USAGE   = '''Usage: !help [<module_name> | all]
Either list all the modules or provide the usage message for a particular
module.
'''

# Command -----------------------------------------------------------------------

def command(bot, nick, message, channel, module_name):
    if module_name == 'all':
        responses = sorted([m.NAME for m in bot.modules.values()])
        return bot.format_responses(responses, nick, channel)

    for module in bot.modules.values():
        if module.NAME == module_name:
            return bot.format_responses(module.USAGE.splitlines(), nick, channel)

    return None

# Register ----------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: ---------------------------------
