''' test bobbit.bot '''

import asyncio
import collections
import unittest

from bobbit.bot import Bobbit

# Test Cases

class BobbitTestCase(unittest.TestCase):

    def test_00_run(self):
        bobbit = Bobbit()
        asyncio.run(bobbit.run())
