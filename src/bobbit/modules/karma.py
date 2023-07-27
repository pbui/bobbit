# karma.py

# Metadata

NAME    = 'karma'
ENABLE  = True
PATTERN = r'^!karma\s+(?P<op>-d|-a|-s)\s+(?P<target>(?:\w+\s?){1,5})$|(?P<shorttarget>[^\s]+)(?P<shortop>[+-]{2})$' # captures '!karma <-d | -a | -s> <1-5 words>' and '<word/nick><++/-->'
USAGE   = '''Usage: <nick/word><++/--> OR !karma [-d | -a | -s] <nick | word/phrase>
This displays, adds, or subtracts karma for the specified nick or word/phrase. Phrases may be up to 5 words.
Example:
    > macos++
    macos now has 1 karma.

    > sussy--
    sussy now has -13 karma.

    > !karma -d lug
    'lug' now has 420 karma.

    > !karma -a AndroidKitKat
    'AndroidKitKat' now has 69 karma.

    > !karma -s wow systems really sucks
    'wow systems really sucks' now has -69420 karma.
'''

# Command

async def karma(bot, message, op, target, shortop, shorttarget):
    # Process short op and target
    if shortop and shorttarget:

        # convert short to long opt
        if shortop == '++':
            op = '-a'
        else:
            op = '-s'

        # move target
        target = shorttarget

    # strip target (in case of extra whitespace, etc.)
    target = target.strip()

    # Process display operation
    if op == '-d':

        # target is a nick and has karma
        if target in bot.users and bot.users[target]['karma']:
            karma = bot.users[target]['karma']

        # target is not a nick and has karma (see comment below for explanation of @karma@)
        elif target in bot.users['@karma@'] and bot.users['@karma@'][target]:
            karma = bot.users['@karma@'][target]

        else: # target has no karma
            return message.with_body(
                bot.client.format_text(
                    '{bold}' + target + '{bold} has no karma.'
                )
            )

        # return karma if target has any
        return message.with_body(
                bot.client.format_text(
                    '{bold}' + target + '{bold} has {color}' + ('{green}' if karma >= 0 else '{red}') + str(karma) + ' karma{color}.'
                )
            )

    else: # Process add and subtract karma operations

        # Prevent users from modifying their own karma
        # Or the karma of a phrase mentioning them
        if message.nick in target:
            return

        # Compute karma
        dkarma = 1 if op == '-a' else -1

        if target in bot.users: # Nick
            karma = bot.users[target]['karma'] = bot.users[target].get('karma', 0) + dkarma
        else:
            # Word/Phrase (hack using @karam@ user); this is the dummy karma
            # user, which has an extra dict of (word : karma) mappings
            user  = '@karma@'

            if user not in bot.users:
                bot.users[user] = {}

            karma = bot.users[user][target] = bot.users[user].get(target, 0) + dkarma

        return message.with_body(
            bot.client.format_text(
                '{bold}' + target + '{bold} now has {color}' + ('{green}' if karma >= 0 else '{red}') + str(karma) + ' karma{color}.'
            )
        )

# Register

def register(bot):
    return (
        ('command', PATTERN, karma),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
