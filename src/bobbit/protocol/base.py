''' bobbit.protocol.base '''

class BaseClient():

    async def connect(self):
        raise NotImplementedError

    async def send_message(self, message):
        raise NotImplementedError

    async def recv_message(self):
        raise NotImplementedError

    @staticmethod
    def format_text(text, *args, **kwargs):
        FORMAT_CODES = {
            'bold'       : '',
            'B'          : '',
            'color'      : '',
            'C'          : '',
            'black'      : '',
            'blue'       : '',
            'green'      : '',
            'red'        : '',
            'brown'      : '',
            'magenta'    : '',
            'orange'     : '',
            'yellow'     : '',
            'lightgreen' : '',
            'cyan'       : '',
            'lightcyan'  : '',
            'lightblue'  : '',
            'pink'       : '',
            'gray'       : '',
            'lightgray'  : '',
            'default'    : '',
        }
        kwargs.update(FORMAT_CODES)
        return text.format(*args, **kwargs)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
