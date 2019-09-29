# -*- coding: utf-8 -*-
"""Add a remote host to host file"""

import sys
import json
import argparse
import logging
from loon.skeleton import __host_file__, setup_logging
from loon.utils import create_parentdir, isfile, isdir

_logger = logging.getLogger(__name__)

def hostadd(username, host, port=22, hostfile=__host_file__, _logger = _logger):
    info = [username, host, port]
    _logger.info("Checking if host file exists...")
    if not isfile(hostfile):
        _logger.info("Creating parent directory for host file...")
        # Create parent dir if hostfile does not exist
        create_parentdir(hostfile)
        cfg = {'current':info, 'available':[info]}
        _logger.info("Saving host info to file...")
        with open(hostfile, 'w') as f:
            json.dump(cfg, f)
        print("=> Added successfully!") 
    else:
        _logger.info("Reading existed host file...")
        with open(hostfile, 'r') as f:
            cfg = json.load(f)

        _logger.info("Checking duplicate of host info...")
        exist_flag = False
        for h in cfg['available']:
            if h == info:
                exist_flag = True
        if exist_flag:
            print("=> Input host exists. Will not change.")
        else:
            _logger.info("Updating info and saving to file...")
            cfg['available'].append(info)
            with open(hostfile, 'w') as f:
                json.dump(cfg, f)

            print("=> Added successfully!") 
    return 0

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Add a remote host")
    parser.add_argument(
        "-u",
        "--user",
        dest = "username",
        help = "remote host username, e.g. wsx"
    )
    parser.add_argument(
        "-r",
        "--host",
        dest = "host",
        help = "remote host ip, e.g. 10.19.24.13"
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        help="remote host port, default is 22",
        default=22,
        type=int)
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
    _logger.info("Starting to add host...")
    hostadd(args.username, args.host, args.port)
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()




