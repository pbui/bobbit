''' bobbit.message '''

import time

class Message():

    def __init__(self, body, nick=None, channel=None, notice=False, highlighted=False, timestamp=None):
        self.body        = body
        self.nick        = nick
        self.channel     = channel
        self.notice      = notice
        self.highlighted = highlighted
        self.timestamp   = timestamp or time.time()

    def copy(self, body=None, nick=None, channel=None, notice=None, highlighted=None, timestamp=None):
        notice_truthy = notice
        highlighted_truthy = highlighted

        if notice is None:
            notice_truthy = self.notice

        if highlighted is None:
            highlighted_truthy = self.highlighted

        return Message(
            body        = body        or self.body,
            nick        = nick        or self.nick,
            channel     = channel     or self.channel,
            notice      = notice_truthy,
            highlighted = highlighted_truthy,
            timestamp   = timestamp   or self.timestamp,
        )

    def with_body(self, body):
        return self.copy(body=body)

    def with_highlight(self, highlighted=True):
        return self.copy(highlighted=highlighted)

    def __str__(self):
        return f'[{self.channel}] {self.nick} {self.body}'
