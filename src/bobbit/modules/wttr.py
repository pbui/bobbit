# wttr.py

'''
# Configuration

The wttr module reads from the weather.yaml file stored in bobbit's
configuration directory and expects the following values:

    default:    This is the default zip code
'''

import logging
import json

# Metadata

NAME    = 'wttr'
ENABLE  = True
PATTERN = r'^!wttr\s*(?P<location>.+)*$'
USAGE   = '''Usage: ![wttr] <location>
Given a location, this returns the current weather for that location.

Examples:
    > !wttr                 # Default location
    > !wttr 92867
    > !wttr Rome, Italy
'''


# Constants

LOCATIONS = {
    '#lug': '46556', # Notre Dame, IN
}
DEFAULT_LOCATION = LOCATIONS['#lug']
WTTR_URL         = 'https://wttr.in/'

# Functions

async def retrieve_wttr_data(bot, location):
    url     = WTTR_URL + str(location).replace(', ', ',')
    params  = {
        'format': 'j1'
    }

    async with bot.http_client.get(url, params=params) as response:
        try:
            return await response.json()
        except json.decoder.JSONDecodeError as e:
            logging.warning('Unable to get weather data: %s', e)
            return {}

# Commands

async def wttr(bot, message, location=None):
    location = location or LOCATIONS.get(message.channel, DEFAULT_LOCATION)
    data     = await retrieve_wttr_data(bot, location)
    if not data:
        return message.with_body('No results')

    try:
        current   = data['current_condition'][0]
        geography = data['nearest_area'][0]
        area      = geography['areaName'][0]['value']
        region    = geography['region'][0]['value']
        country   = geography['country'][0]['value']

        if country == 'United States of America':
            city = f'{area}, {region}'
        else:
            city = f'{area}, {country}'

        return message.with_body(bot.client.format_text(
            '{bold}Weather{bold} for {bold}{city}{bold}: {temp}°F ({I}feels like {feels}°F{I}), {weather}',
            city     = city,
            temp     = current['temp_F'].strip(),
            feels    = current['FeelsLikeF'].strip(),
            weather  = current['weatherDesc'][0]['value'].strip(),
        ))
    except (KeyError, IndexError):
        return message.with_body('Invalid results')

# Register

def register(bot):
    global DEFAULT_LOCATION

    config           = bot.config.load_module_config('weather')
    DEFAULT_LOCATION = config.get('default', LOCATIONS['#lug'])

    return (
        ('command', PATTERN, wttr),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
