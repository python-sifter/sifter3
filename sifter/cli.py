from argparse import ArgumentParser
import email
import os
import logging
import sys
import json

import sifter.parser


def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument('rulefile')
    arg_parser.add_argument('messagefile')
    args = arg_parser.parse_args()

    if not os.path.isfile(args.rulefile):
        logging.error("rulefile '%s' does not exist", args.rulefile)
        sys.exit(1)

    if not os.path.isfile(args.messagefile):
        logging.error("mail message '%s' does not exist", args.messagefile)
        sys.exit(1)

    rules = sifter.parser.parse_file(open(args.rulefile))
    msg = email.message_from_file(open(args.messagefile))
    msg_actions = rules.evaluate(msg)
    print(json.dumps(msg_actions, indent=4))
