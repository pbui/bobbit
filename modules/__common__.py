# __common__.py: ---------------------------------------------------------------

import tornado.httpclient

# Short URLs -------------------------------------------------------------------

def shorten_url(url):
    request = tornado.httpclient.HTTPRequest(
        url    = 'https://yld.me/url',
        method = 'POST',
        body   = url,
    )
    result  = tornado.httpclient.HTTPClient().fetch(request)

    try:
        return result.body.decode().strip()
    except AttributeError:
        return url 

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------
