# metar.py

import logging
import re

# Metadata

NAME    = 'metar'
ENABLE  = True
USAGE   = '''Usage: !metar <id> <date>
Given a station ID, produce the METeorological Aerodrome Report. 
Date is in format yyyymmddhhnn

Examples:
    > !metar                    # Default location
    > !metar kphx               # Phoenix Sky Harbor
    > !metar ksbn 202110271235  # South Bend 2021-10-27 at 12:35
'''

PATTERN = r'^!metar (?P<ids>(".+")|([^\s]+)) (?P<date>(".+")|([^\s]+))$'

# Constants

DEFAULT_ID = 'ksbn'
METAR_URL_BASE = 'https://aviationweather.gov/metar/data?'
METAR_URL_EXT = 'format=raw&hours=0&taf=off&layout=off'
EXTRACT = r'<code>(.*)</code>'

# Functions

async def get_metar_data(bot, ids, date):
    url = METAR_URL_BASE

    if ids:
        url = url + f'ids={ids}&'
    else:
        url = url + f'ids={DEFAULT_ID}&'

    url = url + METAR_URL_EXT

    if date:
        url = url + f'&date={date}'

    async with bot.http_client.get(url) as response:
        return await response.text()

async def metar(bot, message, ids=None, date=None):
    data    = await get_metar_data(bot, ids, date)

    metar = re.findall(EXTRACT, data)

    if '<strong>No METAR found' in data or not metar:
        return message.with_body('No results')

    return message.with_body(metar[0])

# Register

def register(bot):
    return (
        ('command', PATTERN, metar),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
