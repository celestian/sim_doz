#!/usr/bin/env python3

"""sim_jop
Usage:
  sim_jop schema prepare <area.yaml>
  sim_jop schema check <area.yaml>
  sim_jop schema show <area.yaml>
  sim_jop (-h | --help)
  sim_jop --version
Options:
 -h --help     Show this screen.
 --version     Show version.
"""

from docopt import docopt
import logging

from sim_jop.railway.schema import Schema, prepare_schema
from sim_jop.module import start_application


def main():
    """
    Entry point
    """

    args = docopt(__doc__, version='sim_jop 0.0.1')

    logging.basicConfig(level=logging.INFO)

    if args['schema'] and args['prepare']:
        prepare_schema(args['<area.yaml>'])

    if args['schema'] and args['check']:
        Schema(args['<area.yaml>'])

    if args['schema'] and args['show']:
        start_application(args)


if __name__ == '__main__':
    main()
