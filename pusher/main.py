from __future__ import print_function
import sys
import json
import os

import configargparse
import pywebpush


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
    parser.add_argument('--storage', help='Credential storage file',
                        default='creds.txt', type=str)
    parser.add_argument('--topic', help='Message topic', default=None,
                        type=str)
    parser.add_argument('--ttl', help='Message time to live', default=300,
                        type=int)
    parser.add_argument('--msg', help='message body to send', default=None,
                        type=str, required=True)
    return parser


def error(*args, **kwargs):
    print (*args, file=sys.stderr, **kwargs)


def load_subscription(args):
    """Load the subscription information from a well known file.

    """
    return json.loads(open(args.storage, 'r').read())


def main(sysargs=None):
    if not sysargs:
        sysargs = sys.argv[1:]
    args = set_args().parse_args(sysargs)
    try:
        sub_info = load_subscription(args)
    except (IOError, ValueError) as x:
        error("No valid subscription file found.", x)
        return
    try:
        if args.topic:
            if ' ' in args.topic or '"' in args.topic or '"' in args.topic:
                raise Exception("don't use quotes or spaces in your topics")
            topic = args.topic.strip('"\'')
            # The only thing that separates a subscription update from a
            # topic update, is a header.
            pywebpush.WebPusher(sub_info).send(
                args.msg,
                headers={"topic": topic},
                ttl=args.ttl,
            )
        else:
            pywebpush.WebPusher(sub_info).send(
                args.msg,
                ttl=args.ttl,
            )
    except Exception as x:
        error("Could not send message:", x)
        return


if __name__ == '__main__':
    main(sys.argv[1:])
