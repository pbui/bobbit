''' bobbit.http_client '''

import aiohttp

class HTTPClient(aiohttp.ClientSession):
    ''' Wrapper class for aiohttp.ClientSession that supports individual
    request timeouts. '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
            'Connection': 'keep-alive',
        }, **kwargs)

    def get(self, *args, **kwargs):
        ''' https://github.com/aio-libs/aiohttp/issues/3203 '''
        kwargs['timeout'] = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=10)
        return super().get(*args, **kwargs)
