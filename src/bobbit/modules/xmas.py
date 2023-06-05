# xmas.py

import datetime

# Metadata

NAME    = 'xmas'
ENABLE  = True
PATTERN = r'^!(?P<day>(xmas|fall|spring|graduation))\s*$'
USAGE   = '''Usage: !xmas
This prints out the number of days until Christmas.
'''

# Constants

DAYS = {
    'xmas': (
        'Christmas',
        lambda now: \
            datetime.datetime(year=now.year+1, month=12, day=25) - \
            datetime.datetime(year=now.year, month=now.month, day=now.day),
            'Merry Christmas'
    ),
    'fall': (
        'Fall 2023',
        lambda now: \
            datetime.datetime(year=2023, month=8, day=22) - \
            datetime.datetime(year=now.year, month=now.month, day=now.day),
        'Good luck'
    ),
    'spring': (
        'Spring 2024',
        lambda now: \
            datetime.datetime(year=2024, month=1, day=16) - \
            datetime.datetime(year=now.year, month=now.month, day=now.day),
        'Good luck'
    ),
    'graduation': (
        'Graduation',
        lambda now: \
            datetime.datetime(year=2024, month=5, day=19) - \
            datetime.datetime(year=now.year, month=now.month, day=now.day),
        'Congratulations'
    ),
}

# Command

async def xmas(bot, message, day):
    day_name, day_delta, day_message = DAYS[day]
    now = datetime.datetime.now()
    delta = day_delta(now)

    # Handle leap year
    if int(now.year+1) % 4 == 0:
        daysleft = delta.days % 366
    else:
        daysleft = delta.days % 365

    # Return response based on number of days left
    if daysleft > 0:
        return message.with_body(f'{daysleft} {"day" if daysleft == 1 else "days"} until {day_name}')
    else:
        return message.with_body(f'0 days left! {day_message}!')

# Register

def register(bot):
    return (
        ('command', PATTERN, xmas),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
