''' bobbit.protocol.local '''

import asyncio
import os
import sys

from bobbit.protocol.base import BaseClient
from bobbit.message       import Message

class LocalClient(BaseClient):

    def __init__(self, *args, **kwargs):
        self.nick = kwargs.get('nick', 'bobbit')

    async def connect(self):
        pass

    async def send_message(self, message):
        sys.stdout.write(f'=> {message.body}\n')

    async def recv_message(self):
        await asyncio.sleep(0.1)
        sys.stdout.write(f'<= ')
        sys.stdout.flush()
        return Message(
            body    = sys.stdin.readline().rstrip(),
            nick    = os.environ['USER'],
            channel = '#mock',
        )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
