# metar.py

# Metadata

NAME = 'metar'
ENABLE = True
USAGE = '''Usage: ![metar|taf] <id>
Given a station ID, produce the METeorological Aerodrome Report or the terminal
aerodrome forecast.

Examples:
    > !metar                    # Default location
    > !taf kphx                 # Phoenix Sky Harbor
'''

METAR_PATTERN = r'^!metar\s*(?P<ids>[a-zA-Z]+)*\s*(?P<date>[0-9]+)*$'
TAF_PATTERN = r'^!taf\s*(?P<ids>[a-zA-Z]+)*\s*(?P<date>[0-9]+)*$'

DEFAULT_ID = 'ksbn'
METAR_URL_BASE = 'https://aviationweather.gov/cgi-bin/data/metar.php?'
METAR_URL_EXT = '&hours=0&sep=true'


async def get_metar_data(bot, ids, include_taf=False):
    url = METAR_URL_BASE
    url = url + f'ids={ids}&' if ids else url + f'ids={DEFAULT_ID}&'
    url = url + METAR_URL_EXT

    if include_taf:
        url = url + '&taf=true'

    async with bot.http_client.get(url) as response:
        return await response.text()


async def metar(bot, message, ids=None, include_taf=False):
    text = await get_metar_data(bot, ids, include_taf)
    text = text.strip()

    if include_taf:
        return text

    if not text:
        return message.with_body('No results')

    return message.with_body(text)


async def taf(bot, message, ids=None):
    text = await metar(bot, message, ids, True)
    text = 'No results' if not text else text[text.index('\n\n')+2:]

    return message.with_body(text)


def register(bot):
    return (
        ('command', METAR_PATTERN, metar),
        ('command', TAF_PATTERN, taf)
    )
