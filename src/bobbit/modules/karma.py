# karma.py

# Metadata

NAME    = 'karma'
ENABLE  = True
PATTERN = r'^!karma\s+(?P<op>-d|-a|-s)\s+(?P<target>(?:\w+\s?){1,5})$' # captures '!karma <-d | -a | -s> <1-5 words>'
USAGE   = '''Usage: !karma [-d | -a | -s] <nick | word/phrase>
This displays, adds, or subtracts karma for the specified nick or word/phrase. Phrases may be up to 5 words.
Example:
    > !karma -d lug
    'lug' now has 420 karma.

    > !karma -a AndroidKitKat
    'AndroidKitKat' now has 69 karma.

    > !karma -s wow systems really sucks
    'wow systems really sucks' now has -69420 karma.
'''

# Command

async def karma(bot, message, op, target):
    # Process display operation
    if op == '-d':

        if target in bot.users and bot.users[target]['karma']: # target is a nick and has karma
            karma = bot.users[target]['karma']
            return message.with_body(
                bot.client.format_text(
                    '{bold}' + ('\'' + target + '\'') + '{bold} has {color}' + ('{green}' if karma >= 0 else '{red}') + str(karma) + ' karma {color}.'
                )
            )
        elif target in bot.users['@karma@'] and bot.users['@karma@'][target]: # target is not a nick and has karma (see comment below for explanation of @karma@)
            karma = bot.users[target]['karma']
            return message.with_body(
                bot.client.format_text(
                    '{bold}' + ('\'' + target + '\'') + '{bold} has {color}' + ('{green}' if karma >= 0 else '{red}') + str(karma) + ' karma {color}.'
                )
            )
        else: # target has no karma
            return message.with_body(
                bot.client.format_text(
                    '{bold}' + ('\'' + target + '\'') + '{bold} has no karma.'
                )
            )
    else: # Process add and subtract karma operations

        # Prevent users from modifying their own karma
        # Or the karma of a phrase mentioning them
        if message.nick in target:
            return

        # Compute karma
        dkarma = 1 if op == '-a' else -1

        if target in bot.users:   # Nick
            karma = bot.users[target]['karma'] = bot.users[target].get('karma', 0) + dkarma
        else:                   # Word/Phrase (hack using @karam@ user) <- pnutz left this here like it's not a dirty hack
            user  = '@karma@'   # to elaborate, this is the dummy karma user, which has an extra dict of (word : karma) mappings

            if user not in bot.users:
                bot.users[user] = {}

            karma = bot.users[user][target] = bot.users[user].get(target, 0) + dkarma

        return message.with_body(
            bot.client.format_text(
                '{bold}' + ('\'' + target + '\'') + '{bold} now has {color}' + ('{green}' if karma >= 0 else '{red}') + str(karma) + ' karma {color}.'
            )
        )

# Register

def register(bot):
    return (
        ('command', PATTERN, karma),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
