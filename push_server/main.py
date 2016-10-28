import os
import sys

import configargparse
import cyclone.web
from twisted.internet import reactor

from push_server.log import LogObserver
from push_server.handler import MainHandler

PAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "page")


def set_args():
    # type: () -> configargparse.ArgumentParser
    """Read in the args

    """
    parser = configargparse.ArgumentParser(
        default_config_files=["push_server.ini"],
    )
    parser.add_argument('--config', help='Common configuration file path',
                        dest='config_file', is_config_file=True)
    parser.add_argument('--debug', '-d', help="Debug info", default=False,
                        action="store_true")
    parser.add_argument('--port', '-p', help="Port to monitor",
                        default=8200, type=int)
    parser.add_argument('--storage', help='Credential storage file',
                        default='creds.txt', type=str)

    return parser


def main(sysargs=None):
    # type: (dict)
    if not sysargs:
        sysargs = sys.argv[1:]
    args = set_args().parse_args(sysargs)
    options = dict(args=args, path=PAGE_PATH, default_filename="index.html")
    site = cyclone.web.Application([(r'/(.*)', MainHandler, options)])
    LogObserver().start()
    reactor.listenTCP(args.port, site)
    reactor.run()

if __name__ == '__main__':
    main(sys.argv[1:])