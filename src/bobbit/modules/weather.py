# weather.py

'''
# Configuration

The weather module reads from the weather.yaml file stored in bobbit's
configuration directory and expects the following values:

    default:    This is the default zip code
'''

import logging
import re

# Metadata

NAME    = 'weather'
ENABLE  = True
USAGE   = '''Usage: ![weather|forecast] <zipcode>
Given a zipcode, this returns the current weather or the daily forecast for
that location.

Examples:
    > !weather          # Default location
    > !forecast 46556   # Specific zip code
'''

WEATHER_RX  = r'^!weather\s*(?P<zipcode>\d{5})*$'
FORECAST_RX = r'^!forecast\s*(?P<zipcode>\d{5})*$'

# Constants

ZIPCODE   = {
    '#nd-cse' : 46556, # Notre Dame, IN
    '#ndlug'  : 46556, # Notre Dame, IN
    '#lug'    : 46556, # Notre Dame, IN
    '#uwec-cs': 54702, # Eau Claire, WI
}
DEFAULT_ZIPCODE = None
WEATHER_GOV_URL = 'https://forecast.weather.gov'

# Functions

async def retrieve_weather_data(bot, zipcode):
    url     = WEATHER_GOV_URL + '/zipcity.php'
    params  = {
        'inputstring': zipcode
    }

    async with bot.http_client.get(url, params=params) as response:
        try:
            text     = await response.text()
            xml_url  = re.findall(r'<a href="(MapClick[^"]+dwml)"', text)[0]
            json_url = WEATHER_GOV_URL + '/' + xml_url.replace('dwml', 'json')

            logging.debug('JSON URL: %s', json_url)
        except IndexError as e:
            logging.warning('Unable to get weather data: %s', e)
            return {}

    async with bot.http_client.get(json_url) as response:
        return await response.json()

def get_location(data):
    location = data['location']['areaDescription']
    for prefix in re.findall(r'(\d+ Miles [ENSW]+)', location):
        location = location.replace(prefix, '')
    return location.strip()

# Commands

async def weather(bot, message, zipcode=None):
    zipcode = zipcode or ZIPCODE.get(message.channel, DEFAULT_ZIPCODE)
    data    = await retrieve_weather_data(bot, zipcode)
    if not data:
        return message.with_body('No results')

    location = get_location(data)
    current  = data['currentobservation']

    return message.with_body(bot.client.format_text(
        '{bold}Weather{bold} for {bold}{location}{bold}: {temp}°F, {weather}',
        location = location,
        temp     = current['Temp'],
        weather  = current['Weather'],
    ))

async def forecast(bot, message, zipcode=None):
    zipcode = zipcode or ZIPCODE.get(message.channel, DEFAULT_ZIPCODE)
    data    = await retrieve_weather_data(bot, zipcode)
    if not data:
        return message.with_body('No results')

    location = get_location(data)
    text     = data['data']['text']

    return message.with_body(bot.client.format_text(
        '{bold}Forecast for {bold}{location}{bold}: {bold}Today{bold}: {today} {bold}Tonight{bold}: {tonight}',
        location = location,
        today    = text[0].strip(),
        tonight  = text[1].strip(),
    ))

# Register

def register(bot):
    global DEFAULT_ZIPCODE

    config          = bot.config.load_module_config('weather')
    DEFAULT_ZIPCODE = config.get('default', ZIPCODE['#lug'])

    return (
        ('command', WEATHER_RX , weather),
        ('command', FORECAST_RX, forecast),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
