''' test bobbit.bot '''

import os
import sys
import unittest

sys.path.insert(0, 'src')

from bobbit.bot               import Bobbit
from bobbit.message           import Message
from bobbit.modules.eightball import register, eightball, RESPONSES

# Test Cases

class EightballTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_00_eightball(self):
        message = await eightball(None, Message('!8ball'), None)
        for _ in range(len(RESPONSES)):
            self.assertTrue(isinstance(message, Message))
            self.assertTrue(any(message.body in r for r in RESPONSES))
