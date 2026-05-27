''' bobbit.utils '''

import asyncio
import re

async def shorten_url(http_client, url, attempts=5):
    for b in  ('i.redd.it', ):
        if b in url:
            return url

    for _ in range(attempts):
        async with http_client.post('https://yld.me/url', data=url.encode()) as response:
            try:
                result = (await response.text()).strip()
            except AttributeError:
                result = None

            if result and result != '<html>':
                return result

    return url

async def curl(url):
    command = ['curl', '-sL', url]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE
    )
    return (await process.communicate())[0].decode()

def elapsed_time(current, previous):
    elapsed = current - previous
    units   = (
        ('seconds', 60),
        ('minutes', 60),
        ('hours'  , 24),
        ('days'   , 7),
        ('weeks'  , 52),
    )
    for unit, step in units:
        if elapsed < step:
            break
        elapsed /= step

    return '{:0.2f} {}'.format(elapsed, unit)

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
