''' bobbit.tests.mock_client '''

import asyncio
import os
import sys

sys.path.insert(0, os.curdir)

from bobbit.bot   import Bobbit
from bobbit.tests import MockClient

def mock_client():
    bot = Bobbit()
    bot.client = MockClient
    asyncio.run(bot.run())

if __name__ == '__main__':
    mock_client()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
