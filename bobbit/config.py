''' bobbit.config '''

import logging
import logging.handlers
import os
import yaml

from bobbit.protocol import IRCClient, SlackClient

class Configuration():
    ''' Load configuration from YAML file '''

    def __init__(self, config_dir=None, log_path=None, debug=False):
        self.config_dir  = os.path.expanduser(config_dir or '~/.config/bobbit')
        self.config_path = os.path.join(self.config_dir, 'bobbit.yaml')
        self.modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))

        if os.path.exists(self.config_path):
            config = yaml.safe_load(open(self.config_path))
        else:
            config = {}

        log_format = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
        log_level  = logging.DEBUG if config.get('debug', debug) else logging.INFO
        logging.basicConfig(
            format   = log_format,
            datefmt  = '%Y-%m-%d %H:%M:%S',
            level    = log_level,
        )

        logger = logging.getLogger()

        if log_path:
            log_handler = logging.handlers.RotatingFileHandler(
                log_path, maxBytes=1024*1024, backupCount=10
            )
            log_handler.setFormatter(logging.Formatter(log_format))
            log_handler.setLevel(log_level)
            logger.addHandler(log_handler)

        logger.info('Configuration Directory: %s', self.config_dir)
        logger.info('Configuration Path:      %s', self.config_path)
        logger.info('Modules Path:            %s', self.modules_dir)

        self.nick    = config.get('nick'       , 'bobbit')
        self.owners  = config.get('owners'     , [os.environ['USER']])
        self.use_ssl = config.get('ssl'        , False)

        logger.info('Nick:           %s', self.nick)
        logger.info('Owners:         %s', ', '.join(self.owners))
        logger.info('SSL:            %s', self.use_ssl)

        if config.get('token', None):
            self.client      = SlackClient
            self.host        = config.get('host'    , 'api.slack.com')
            self.port        = 443
            self.password    = config.get('token'   , '')
        else:
            self.client      = IRCClient
            self.host        = config.get('host'    , 'irc.freenode.net')
            self.port        = config.get('port'    , 6667)
            self.password    = config.get('password', '')

        self.channels = config.get('channels', [])
        logger.info('Server:         %s:%d', self.host, self.port)
        logger.info('Password:       %s'   , self.password)
        logger.info('Channels:       %s'   , ', '.join(self.channels))

    def get_config_path(self, file_name):
        return os.path.join(self.config_dir, file_name)

    def load_module_config(self, module_name):
        config_path = self.get_config_path(module_name + '.yaml')
        try:
            config_data = yaml.safe_load(open(config_path))
        except (IOError, OSError, yaml.parser.ParserError) as e:
            logging.warning('Unable to open configuration file %s: %s', config_path, e)
            config_data = {}

        return config_data

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
