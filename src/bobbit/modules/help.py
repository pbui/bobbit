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

    # Prevent bobbit spam when listing all commands
    safety_switch = False

    if not module_name or module_name == 'all':
        safety_switch = True
        responses = sorted([m.NAME for m in bot.modules])
    else:
        for module in bot.modules:
            if module.NAME == module_name:
                responses = module.USAGE.splitlines()

    # Suggest responses if none match
    if not responses:
        safety_switch = True
        responses = sorted([m.NAME for m in bot.modules if module_name in m.NAME])

    if safety_switch:
        formatted_response = ", ".join(responses)
        return message.with_body(formatted_response)

    return [message.copy(body=r, notice=True) for r in responses]

# Register

def register(bot):
    return (
        ('command', PATTERN, help),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
