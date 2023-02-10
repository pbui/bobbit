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
    all_modules = {m.NAME: m for m in bot.modules}

    if module_name == 'all' or not module_name:
        return message.with_body(', '.join(sorted(all_modules)))
    
    # Lookup specific help message
    if module_name in all_modules:
        responses = all_modules[module_name].USAGE.splitlines()
        return [message.copy(body=r) for r in responses]

    # If module_name not found, alert user and return command list
    responses = [f'\"{module_name}\" not found. Try these: ',', '.join(sorted(all_modules))]
    return [message.copy(body=r) for r in responses]

# Register

def register(bot):
    return (
        ('command', PATTERN, help),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
