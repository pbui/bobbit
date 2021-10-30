# metar.py

import logging
import re

# Metadata

NAME    = 'metar'
ENABLE  = True
USAGE   = '''Usage: ![metar|taf] <id> <date>
Given a station ID, produce the METeorological Aerodrome Report or the terminal
aerodrome forecast.
Date is in format yyyymmddhhnn

Examples:
    > !metar                    # Default location
    > !taf kphx                 # Phoenix Sky Harbor
    > !taf ksbn 202110271235    # South Bend 2021-10-27 at 12:35
'''

# Thanks for the regex help, pbui
METAR_PATTERN = r'^!metar\s*(?P<ids>[a-zA-Z]+)*\s*(?P<date>[0-9]+)*$'
TAF_PATTERN = r'^!taf\s*(?P<ids>[a-zA-Z]+)*\s*(?P<date>[0-9]+)*$'

# Constants

DEFAULT_ID = 'ksbn'
METAR_URL_BASE = 'https://aviationweather.gov/metar/data?'
METAR_URL_EXT = 'format=raw&hours=0&taf=off&layout=off'
EXTRACT = r'<code>(.*)</code>'

# Functions

async def get_metar_data(bot, ids, date, taf=False):
    url = METAR_URL_BASE

    if ids:
        url = url + f'ids={ids}&'
    else:
        url = url + f'ids={DEFAULT_ID}&'

    url = url + METAR_URL_EXT

    if taf:
        url = url + '&taf=on'

    if date:
        url = url + f'&date={date}'

    async with bot.http_client.get(url) as response:
        return await response.text()

async def metar(bot, message, ids=None, date=None):
    data    = await get_metar_data(bot, ids, date, False)

    metar = re.findall(EXTRACT, data)

    if '<strong>No METAR found' in data or not metar:
        return message.with_body('No results')

    return message.with_body(metar[0])

async def taf(bot, message, ids=None, date=None):
    data    = await get_metar_data(bot, ids, date, True)

    metar = re.findall(EXTRACT, data)

    if '<strong>No METAR found' in data or len(metar) < 2:
        return message.with_body('No results')

    taf = re.sub('<br/>&nbsp;&nbsp;', '\n    ', metar[1])
    return message.with_body(taf)

# Register

def register(bot):
    return (
        ('command', METAR_PATTERN, metar),
        ('command', TAF_PATTERN, taf)
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
