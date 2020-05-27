''' bobbit.protocol.mock '''

import asyncio
import os
import sys

from bobbit.protocol.base import BaseClient
from bobbit.message       import Message

class MockClient(BaseClient):

    def __init__(self, *args, **kwargs):
        pass

    async def connect(self):
        pass

    async def send_message(self, message):
        sys.stdout.write(str(message))
        sys.stdout.write('\n')

    async def recv_message(self):
        await asyncio.sleep(0.5)
        return Message(
            body    = sys.stdin.readline().rstrip(),
            nick    = os.environ['USER'],
            channel = '#mock',
        )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
