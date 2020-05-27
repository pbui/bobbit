# urbandictionary.py

# Metadata

NAME    = 'urbandictionary'
ENABLE  = True
PATTERN = '^!ud (?P<query>.*$)'
USAGE   = '''Usage: !ud <query>
Given a search query, this returns the first result from Urban Dictionary
Example:
    > !ud pancakes
'''

# Constants

UD_URL      = 'http://api.urbandictionary.com/v0/define'
UD_TEMPLATE = '{color}{green}{word}{color}: {bold}{definition}{bold}; an example is: {color}{cyan}{example}{color} @ {color}{blue}{url}{color}'

# Command

async def urbandictionary(bot, message, query=None):
    try:
        query, index = query.rsplit(' ', 1)
        index = int(index)
    except ValueError:
        index = 0

    async with bot.http_client.get(UD_URL, params={'term': query}) as response:
        try:
            data     = (await response.json())['list'][index]
            response = bot.client.format_text(UD_TEMPLATE,
                word       = data['word'],
                definition = data['definition'].strip().replace('\r', ' ').replace('\n', ' '),
                example    = data['example'].strip().replace('\r', ' ').replace('\n', ' '),
                url        = data['permalink'],
            )
        except (IndexError, ValueError):
            response = 'No results'

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, urbandictionary),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
