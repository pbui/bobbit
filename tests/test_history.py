''' Test history module '''

import os
import sys
import unittest

sys.path.insert(0, 'src')

from bobbit.history import History
from bobbit.message import Message

from bobbit.bot         import Bobbit
from bobbit.message     import Message

# Test Cases

class HistoryInsertTestCase(unittest.IsolatedAsyncioTestCase):
    TEST_CHANNEL1 = "foo"
    TEST_CHANNEL2 = "fu"

    TEST_USER1 = "woof"
    TEST_USER2 = "m3ow"

    async def test_insert(self):
        hs = History()
        
        msg1 = Message("bar", channel=self.TEST_CHANNEL1)
        msg2 = Message("baz", channel=self.TEST_CHANNEL1)
        msg3 = Message("qux", channel=self.TEST_CHANNEL1)
        msg4 = Message("bar", channel=self.TEST_CHANNEL2)

        hs.insert(msg1)
        hs.insert(msg2)
        hs.insert(msg4)
        hs.insert(msg3)
        
        chan1 = hs.history.get(self.TEST_CHANNEL1)
        self.assertEqual(len(chan1), 3)
        self.assertEqual(msg1, chan1[0])
        self.assertEqual(msg2, chan1[1])
        self.assertEqual(msg3, chan1[2])
        
        chan2 = hs.history.get(self.TEST_CHANNEL2)
        self.assertEqual(len(chan2), 1)
        self.assertEqual(msg4, chan2[0])

    async def test_history_limit(self):
        hs = History(maxlen=5)

        msg1 = Message("bar", channel=self.TEST_CHANNEL1)
        msg2 = Message("baz", channel=self.TEST_CHANNEL1)
        msg3 = Message("qux", channel=self.TEST_CHANNEL1)
        msg4 = Message("quz", channel=self.TEST_CHANNEL1)
        msg5 = Message("var", channel=self.TEST_CHANNEL1)
        msg6 = Message("ter", channel=self.TEST_CHANNEL1)
        msg7 = Message("daz", channel=self.TEST_CHANNEL1)

        hs.insert(msg1)
        hs.insert(msg2)
        hs.insert(msg3)
        hs.insert(msg4)
        hs.insert(msg5)

        hs.insert(msg6)

        chan1 = hs.history.get(self.TEST_CHANNEL1)

        self.assertEqual(len(chan1), 5)
        self.assertEqual(chan1[0], msg2)
        self.assertEqual(chan1[4], msg6)

        hs.insert(msg7)

        self.assertEqual(chan1[0], msg3)
        self.assertEqual(chan1[4], msg7)


class HistorySearchTestCase(unittest.IsolatedAsyncioTestCase):
    TEST_CHANNEL1 = "foo"
    TEST_CHANNEL2 = "fu"

    TEST_USER1 = "woof"
    TEST_USER2 = "m3ow"

    def setUp(self):
        self.hs = History()

        self.hs.insert(Message("bar", nick=self.TEST_USER1, channel=self.TEST_CHANNEL1))
        self.hs.insert(Message("baz", nick=self.TEST_USER2, channel=self.TEST_CHANNEL1))
        self.hs.insert(Message("arbax", nick=self.TEST_USER2, channel=self.TEST_CHANNEL1))

        self.hs.insert(Message("quz", nick=self.TEST_USER2, channel=self.TEST_CHANNEL2))
        self.hs.insert(Message("qux", nick=self.TEST_USER1, channel=self.TEST_CHANNEL2))

    async def test_no_matches(self):
        matches = []
        for m in self.hs.search(self.TEST_CHANNEL1):
            matches.append(m)
        
        self.assertEqual(len(matches), 0)

    async def test_nick_match(self):
        matches = []
        for m in self.hs.search(self.TEST_CHANNEL1, nick=self.TEST_USER2):
            matches.append(m)
        
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].body, "baz")
        self.assertEqual(matches[1].body, "arbax")

    async def test_pattern_match(self):
        matches = []
        for m in self.hs.search(self.TEST_CHANNEL1, pattern="^ba"):
            matches.append(m)
        
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].body, "bar")
        self.assertEqual(matches[1].body, "baz")

    async def test_reversed_match(self):
        matches = []
        for m in self.hs.search(self.TEST_CHANNEL1, nick=self.TEST_USER2, reverse=True):
            matches.append(m)
        
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].body, "arbax")
        self.assertEqual(matches[1].body, "baz")

    async def test_match_limit(self):
        matches = []
        for m in self.hs.search(self.TEST_CHANNEL1, nick=self.TEST_USER2, limit=1):
            matches.append(m)
        
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].body, "baz")


if __name__ == '__main__':
    unittest.main()
