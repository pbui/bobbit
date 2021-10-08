# help.py

# Metadata

NAME    = 'help'
ENABLE  = True
PATTERN = '^!help\s*(?P<module_name>.*)$'
USAGE   = '''Usage: !help [<module_name> | all]
Either list all the modules or provide the usage message for a particular
module.
'''

# Command

async def help(bot, message, module_name=None):
    responses = []

    if module_name and module_name != 'all':
        for module in bot.modules:
            if module.NAME == module_name:
                responses = module.USAGE.splitlines()
                return [message.copy(body=r, notice=True) for r in responses]
    else:
        responses = sorted([m.NAME for m in bot.modules])

    # Suggest responses if none match
    if not responses:
        responses = sorted([m.NAME for m in bot.modules if module_name in m.NAME])

    return message.with_body(", ".join(responses))

# Register

def register(bot):
    return (
        ('command', PATTERN, help),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
