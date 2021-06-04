# crypto.py

# Metadata

NAME = 'crypto'
ENABLE = True
PATTERN = '^!crypto (?P<symbol>.*)$'
USAGE = '''Usage: !crypto <symbol>
Given a crypto symbol, this returns the pricing information.
Example:
    > !crypto DOGE
    TBD
'''

# Constants

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
API_KEY = None

# Command

async def crypto(bot, message, symbol=None):
    headers = {
       'X-CMC_PRO_API_KEY': API_KEY,
       'Accept': 'application/json',
       'Accept-Encoding': 'deflate, gzip'
    }
    params = { 'symbol': symbol.upper() }
    async with bot.http_client.get(API_URL, params=params, headers=headers) as response:
        try:
            data = await response.json()
            if data['status']['error_code']: # check for non-zero status codes
                raise KeyError

            quote = data['data'][symbol.upper()]['quote']['USD']

            response = bot.client.format_text(
                "{bold}Symbol{bold}: {symbol}, "
                "{color}{magenta}Price{color}: {price:0.2f}, "
                "{color}{green}1-hour{color}: {hour_percent:0.2f}%, "
                "{color}{red}24-hour{color}: {day_percent:0.2f}%, "
                "{color}{cyan}7-day{color}: {week_percent:0.2f}%",
                symbol = symbol.upper(),
                price = quote['price'],
                hour_percent = quote['percent_change_1h'],
                day_percent = quote['percent_change_24h'],
                week_percent = quote['percent_change_7d'],
            )

        except KeyError:
            response = 'No results'

    return message.with_body(response)

# Register

def register(bot):
    global API_KEY
    config = bot.config.load_module_config('crypto')
    API_KEY = config.get('api_key', '')

    if not API_KEY:
        return []

    return (
        ('command', PATTERN, crypto),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
