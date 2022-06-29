# roll.py

import random

# Metadata

NAME    = 'roll'
ENABLE  = True
PATTERN = r'^!roll\s*(?P<num>\d*)?d(?P<size>\d+)$'
USAGE   = '''Usage: !roll <number of dice>d<size of dice>
Rolls some dice.
'''

# Command

async def roll(bot, message, size, num):
    # size must be a number > 0
    try:
        size = int(size)
        if size == 0:
            return
    except ValueError as e:
        return
    # number of dice must be 0 < n <= 100
    try:
        num = int(num)
        if num > 100 or num == 0:
            return
    except ValueError as e:
        num = 1

    rolls = [random.randint(1, size) for d in range(num)]
    output = f"Rolling {num}d{size}: {sum(rolls)}"
    if num > 1:
        output += f", from [{' + '.join(str(r) for r in rolls}]"
    return message.with_body(output)

# Register

def register(bot):
    return (
        ('command', PATTERN, roll),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
