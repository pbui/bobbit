''' bobbit.utils '''

import re

async def shorten_url(http_client, url):
    for b in  ('i.redd.it', ):
        if b in url:
            return url

    async with http_client.post('https://yld.me/url', data=url.encode()) as response:
        try:
            return (await response.text()).strip()
        except AttributeError:
            return url

def parse_options(options, arguments):
    while arguments.startswith('-'):
        try:
            option, arguments = arguments.split(' ', 1)
        except ValueError:
            break

        if option not in options:
            continue

        if isinstance(options.get(option), bool):
            options[option] = True
        else:
            try:
                options[option], arguments = arguments.split(' ', 1)
            except ValueError:
                break

    return options, arguments

def strip_html(s):
    return re.sub('<[^<]+?>', '', s)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
