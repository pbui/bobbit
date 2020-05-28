# stock.py

# Metadata

NAME    = 'stock'
ENABLE  = True
PATTERN = '^!stock (?P<symbol>.*$)'
USAGE   = '''Usage: !stock <symbol>
Given a stock symbol, this returns the daily stock pricing information.
Example:
    > !stock TSLA
    Symbol: TSLA, Price: 815.56, Open: 820.5, High: 826, Low: 811.8, Change: 4.94
'''

# Constants

API_URL = 'https://finnhub.io/api/v1/quote'
API_KEY = None

# Command

async def stock(bot, message, symbol=None):
    params = {'symbol': symbol.upper(), 'token': API_KEY}
    async with bot.http_client.get(API_URL, params=params) as response:
        try:
            data     = await response.json()
            response = bot.client.format_text(
                "{bold}Symbol{bold}: {symbol}, "
                "{color}{magenta}Price{color}: {price}, "
                "{color}{blue}Open{color}: {price_open}, "
                "{color}{green}High{color}: {day_high}, "
                "{color}{red}Low{color}: {day_low}, "
                "{color}{cyan}Change{color}: {day_change:0.2f}",
                symbol     = symbol.upper(),
                price      = data['c'],
                price_open = data['o'],
                day_high   = data['h'],
                day_low    = data['l'],
                day_change = data['o'] - data['c'],
            )
        except KeyError:
            response = 'No results'

    return message.with_body(response)

# Register

def register(bot):
    global API_KEY

    config  = bot.config.load_module_config('stock')
    API_KEY = config.get('api_key', '')

    if not API_KEY:
        return []

    return (
        ('command', PATTERN, stock),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
