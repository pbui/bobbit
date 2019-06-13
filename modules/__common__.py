# __common__.py:

import tornado.httpclient
import tornado.gen

# Nick Wrapper

class PrefixedNick(str):
    def __new__(cls, content):
        self = super().__new__(cls, content)
        self.prefix = True
        return self

# Short URLs

BLACKLIST = (
    'i.redd.it',
)

@tornado.gen.coroutine
def shorten_url(url):
    for b in BLACKLIST:
        if b in url:
            return url

    request = tornado.httpclient.HTTPRequest(
        url    = 'https://yld.me/url',
        method = 'POST',
        body   = url,
    )
    result  = yield tornado.httpclient.AsyncHTTPClient().fetch(request)

    try:
        return result.body.decode().strip()
    except AttributeError:
        return url 

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
