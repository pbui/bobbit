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


def strip_html(s):
    return re.sub('<[^<]+?>', '', s)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
