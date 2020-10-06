''' Test message module '''

import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, 'src')

from bobbit.history import History
from bobbit.message import Message

from bobbit.bot         import Bobbit
from bobbit.message     import Message

# Test Cases

class MessageTestCase(unittest.IsolatedAsyncioTestCase):

    def test_init_no_timestamp(self):
        TEST_DEFAULT_TIME = 1111
        with mock.patch('time.time', mock.MagicMock(return_value=TEST_DEFAULT_TIME)):
            msg = Message("hi")

            self.assertEqual(msg.timestamp, TEST_DEFAULT_TIME)

    def test_init_timestamp(self):
        TEST_TIMESTAMP = 1234

        msg = Message("hi", timestamp = TEST_TIMESTAMP)

        self.assertEqual(msg.timestamp, TEST_TIMESTAMP)
    
    def test_copy_defaults(self):
        test_msg = Message("hi", nick="woof", channel="foo", notice=True)

        copied_msg = test_msg.copy()

        self.assertNotEqual(id(test_msg), id(copied_msg))
        self.assertEqual(test_msg.body, copied_msg.body)
        self.assertEqual(test_msg.nick, copied_msg.nick)
        self.assertEqual(test_msg.channel, copied_msg.channel)
        self.assertEqual(test_msg.notice, copied_msg.notice)
        self.assertEqual(test_msg.highlighted, copied_msg.highlighted)
        self.assertEqual(test_msg.timestamp, copied_msg.timestamp)

    def test_copy(self):
        test_msg = Message("hi", nick="woof", channel="foo", notice=True)

        copied_msg = test_msg.copy(body="hello", channel="fu", notice=False)

        self.assertNotEqual(id(test_msg), id(copied_msg))
        self.assertNotEqual(test_msg.body, copied_msg.body)
        self.assertEqual(test_msg.nick, copied_msg.nick)
        self.assertNotEqual(test_msg.channel, copied_msg.channel)
        self.assertNotEqual(test_msg.notice, copied_msg.notice)
        self.assertEqual(test_msg.highlighted, copied_msg.highlighted)
        self.assertEqual(test_msg.timestamp, copied_msg.timestamp)

    def test_with_body(self):
        test_msg = Message("hi", nick="woof", channel="foo", notice=True, highlighted=True)

        copied_msg = test_msg.with_body("hello")

        self.assertNotEqual(id(test_msg), id(copied_msg))
        self.assertNotEqual(test_msg.body, copied_msg.body)
        self.assertEqual(test_msg.nick, copied_msg.nick)
        self.assertEqual(test_msg.channel, copied_msg.channel)
        self.assertEqual(test_msg.notice, copied_msg.notice)
        self.assertEqual(test_msg.highlighted, copied_msg.highlighted)
        self.assertEqual(test_msg.timestamp, copied_msg.timestamp)

    def test_with_highlight_default(self):
        test_msg = Message("hi", nick="woof", channel="foo")

        copied_msg = test_msg.with_highlight()

        self.assertNotEqual(id(test_msg), id(copied_msg))
        self.assertEqual(test_msg.body, copied_msg.body)
        self.assertEqual(test_msg.nick, copied_msg.nick)
        self.assertEqual(test_msg.channel, copied_msg.channel)
        self.assertEqual(test_msg.notice, copied_msg.notice)
        self.assertTrue(copied_msg.highlighted)
        self.assertEqual(test_msg.timestamp, copied_msg.timestamp)

    def test_with_highlight_false(self):
        test_msg = Message("hi", nick="woof", channel="foo", highlighted=True)

        copied_msg = test_msg.with_highlight(highlighted=False)

        self.assertNotEqual(id(test_msg), id(copied_msg))
        self.assertEqual(test_msg.body, copied_msg.body)
        self.assertEqual(test_msg.nick, copied_msg.nick)
        self.assertEqual(test_msg.channel, copied_msg.channel)
        self.assertEqual(test_msg.notice, copied_msg.notice)
        self.assertFalse(copied_msg.highlighted)
        self.assertEqual(test_msg.timestamp, copied_msg.timestamp)


if __name__ == '__main__':
    unittest.main()
