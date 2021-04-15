# ree.py

# Metadata

NAME    = 'ree'
ENABLE  = True
PATTERN = r'(^!|^|^.*\s)[Rr][Ee]{2,}(\s|$)'
USAGE   = '''Usage: !ree
This reports a leaderboard of users' "ree"s 
and (eventually, not yet implemented) a timedelta since the most recent "ree"
Example:
    > !ree
    Time since last "ree": 15 min (<nickA>)
    Ree-derboard:
    <nickA>     10
    <nickB>     7
    <nickC>     5
'''

# Command

async def ree(bot, message):
    user        = bot.users.get(message.nick, {})
    msg         = []
    leaderboard = []

    # present leaderboard and timedelta
    if message.body.startswith('!'):
        msg.append(message.with_body('Ree-derboard:'))
        for nick, user in bot.users.items():
            if 'rees' in user:
                leaderboard.append((nick, user['rees']))
        msg += [message.with_body(f'\t{x[1]} - {x[0]}') for x in sorted(leaderboard, key=lambda x: x[1], reverse=True)]
        return msg

    # record a "ree" for sender
    if message.nick not in bot.users:
        bot.users[message.nick] = {}
    bot.users[message.nick]['rees'] = bot.users[message.nick].get('rees', 0) + 1
    return message.with_body('Your "ree" has been recorded')


# Register

def register(bot):
    return (
        ('command', PATTERN, ree),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
