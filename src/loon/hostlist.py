# -*- coding: utf-8 -*-
"""List all remote hosts in host file"""

import sys
import json
import argparse
import logging
from loon.skeleton import __host_file__, setup_logging
from loon.utils import create_parentdir, isfile, isdir

_logger = logging.getLogger(__name__)

def hostlist(hostfile = __host_file__, _logger = _logger):
    """List all available hosts in host file"""

    _logger.info("Check host file...")
    if not isfile(__host_file__):
        raise FileNotFoundError("File {} not found".format(__host_file__))
    else:
        with open(__host_file__, 'r') as f:
            cfg = json.load(f)

    #TODO pretty print
    #Ref: http://zetcode.com/python/prettytable/
    _logger.info("Print host list...")
    print("="*36)
    print("username\thost\tport")
    print("="*36)
    for h in cfg['available']:
        if h == cfg['current']:
            print("*", end="")
        print("{0[0]}\t{0[1]}\t{0[2]}".format(h))
    print("="*36)
    print("NOTE: current host marked by *")
    return 0

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="List all available hosts in host file")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    
    return parser.parse_args(args)

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Starting to list hosts...")
    hostlist()
    _logger.info("Script ends here")

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
