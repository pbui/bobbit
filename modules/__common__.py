# __common__.py: ---------------------------------------------------------------

import tornado.httpclient
import tornado.gen

# Short URLs -------------------------------------------------------------------

@tornado.gen.coroutine
def shorten_url(url):
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

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
