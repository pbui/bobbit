# weather.py

'''
# Configuration

The weather module reads from the weather.yaml file stored in bobbit's
configuration directory and expects the following values:

    appid:      This is the Open Weather Map APPID
    default:    This is the default zip code
'''

# Metadata

NAME    = 'weather'
ENABLE  = True
PATTERN = r'^!weather\s*(?P<zipcode>\d{5})*$'
USAGE   = '''Usage: !weather <zip code>
Given a zip code, this returns the current weather for that location
Example:
    > !weather          # Default location
    > !weather 46556    # Specific zip code
'''

# Constants

OWM_URL   = 'https://api.openweathermap.org/data/2.5/weather'
OWM_APPID = None
ZIPCODE   = {
    '#nd-cse' : 46556, # Notre Dame, IN
    '#ndlug'  : 46556, # Notre Dame, IN
    '#lug'    : 46556, # Notre Dame, IN
    '#uwec-cs': 54702, # Eau Claire, WI
}
DEFAULT_ZIPCODE = None

# Command

async def weather(bot, message, zipcode=None):
    zipcode = zipcode or ZIPCODE.get(message.channel, DEFAULT_ZIPCODE)
    params  = {
        'zip':   zipcode,
        'appid': OWM_APPID,
        'units': 'imperial',
    }

    async with bot.http_client.get(OWM_URL, params=params) as response:
        try:
            data     = await response.json()
            temp     = data['main']['temp'] # TODO: Apply colors to temperature
            text     = data['weather'][0]['description']
            response = f'Current weather is {temp}°F, {text.title()}'
        except (KeyError, IndexError, ValueError):
            response = 'No results'

    return message.with_body(response)

# Register

def register(bot):
    global OWM_APPID, DEFAULT_ZIPCODE

    config          = bot.config.load_module_config('weather')
    DEFAULT_ZIPCODE = config.get('default', ZIPCODE['#lug'])
    OWM_APPID       = config.get('appid', None)

    return (
        ('command', PATTERN, weather),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
