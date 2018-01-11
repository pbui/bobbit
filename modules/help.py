# help.py -----------------------------------------------------------------------

# Metadata ----------------------------------------------------------------------

NAME    = 'help'
ENABLE  = True
TYPE    = 'command'
PATTERN0= '^!help$'
PATTERN1= '^!help (?P<module_name>.*)'
USAGE   = '''Usage: !help [<module_name> | all]
Either list all the modules or provide the usage message for a particular
module.
'''

# Command -----------------------------------------------------------------------

def command(bot, nick, message, channel, module_name=None):
    if module_name is None or module_name == 'all':
        response = sorted([m.NAME for m in bot.modules.values()])
        bot.send_response(response, nick, channel, notice=True)

    for module in bot.modules.values():
        if module.NAME == module_name:
            response = module.USAGE.splitlines()
            bot.send_response(response, nick, channel, notice=True)

# Register ----------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN0, command),
        (PATTERN1, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: ---------------------------------
