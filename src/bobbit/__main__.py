''' bobbit.__main__ '''

import argparse
import asyncio
import sys

from bobbit.bot import Bobbit

def Parser():
    parser = argparse.ArgumentParser(
        prog            = 'bobbit',
        description     = 'Simple Asynchronous IRC/Slack Bot',
        formatter_class = lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
        add_help        = False,
    )
    parser.add_argument(
        '--config-dir',
        default = '~/.config/bobbit',
        help    = 'Configuration directory (default: %(default)s)',
    )
    parser.add_argument(
        '--log-path',
        default = None,
        help    = 'Path to log file (default: %(default)s)',
    )
    parser.add_argument(
        '--debug',
        default = False,
        action  = 'store_true',
        help    = 'Enable debug logging (default: %(default)s)',
    )
    parser.add_argument(
        '--local',
        default = False,
        action  = 'store_true',
        help    = 'Enable local client (default: %(default)s)',
    )
    parser.add_argument(
        '-h', '--help',
        action  = argparse._HelpAction,
        help    = 'Show this help message and exit',
    )

    return parser

def main():
    parser = Parser()
    args   = parser.parse_args()
    bobbit = Bobbit(args.config_dir, args.log_path, args.debug, args.local)

    try:
        status = asyncio.run(bobbit.run())
    except KeyboardInterrupt:
        status = 'Interrupted'

    sys.exit(status)

# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
