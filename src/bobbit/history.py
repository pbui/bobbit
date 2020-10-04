# bobbit.history

import collections
import re

# History class

class History():
    ''' The History class keeps track of the messages in each channel using a
    bounded buffer.
    '''

    def __init__(self, history_dir=None, maxlen=100):
        self.history = collections.defaultdict(lambda: collections.deque(maxlen=maxlen))

        # TODO: Checkpoint history and read it back from disk

    def insert(self, message):
        self.history[message.channel].append(message)

    def search(self, channel, nick=None, pattern=None, limit=None, reverse=False):
        if pattern:
            pattern = re.compile(pattern)

        messages = self.history.get(channel, collections.deque())
        if reverse:
            messages.reverse()

        count = 0
        limit = limit or len(messages)
        for message in messages:
            if count == limit:
                break

            if (nick and nick == message.nick) or \
               (pattern and pattern.search(message.body)):
                yield message.with_highlight()
                count += 1

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
