''' Test echo module '''

import os
import sys
import unittest

sys.path.insert(0, 'src')

from bobbit.bot          import Bobbit
from bobbit.message      import Message
from bobbit.modules.echo import register, echo

# Test Cases

class EchoTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_00_echo(self):
        for body in ('hello', 'world', 'quick brown fox'):
            message = await echo(None, Message(body), None)
            self.assertTrue(isinstance(message, Message))
            self.assertEqual(message.body, body)
