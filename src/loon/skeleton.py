# -*- coding: utf-8 -*-
"""
The skeleton of loon package.
Set command in [options.entry_points] section of setup.cfg file
Install with `python setup.py install`
"""

import os
import sys
import argparse
import logging

if __package__ == '' or __package__ is None:  # Use for test
  from __init__ import __version__
  from classes import Host
else:
  from loon import __version__
  from loon.classes import Host

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Be an efficient loon.")

    # Show version info
    parser.add_argument(
        "--version",
        action="version",
        version="loon {ver}".format(ver=__version__))

    # Common arguments
    host_parent_parser = argparse.ArgumentParser(add_help=False)
    host_parent_parser.add_argument(
      '-U', '--username',
      dest='username',
      help='Username for remote host',
      type = str, 
      required=True)
    host_parent_parser.add_argument(
      '-H', '--host',
      dest='host',
      help='IP address for remote host (e.g. 192.168.0.1)',
      type = str,
      required=True)
    host_parent_parser.add_argument(
      '-P', '--port',
      dest="port",
      help='Port for remote host, default is 22', 
      type = int,
      default=22)

    host_parent_parser.add_argument(
      "-v",
      "--verbose",
      dest="loglevel",
      help="set loglevel to INFO",
      action="store_const",
      const=logging.INFO)

    # Subcommands
    subparsers = parser.add_subparsers(
      title='subcommands',
      #description='valid subcommands',
      help="description",
      dest="subparsers_name")

    # Create the parser for the "add" command
    parser_add = subparsers.add_parser(
      'add',
      help="Add a remote host",
      parents=[host_parent_parser])
    parser_add.add_argument(
      '-A',
      '--active',
      dest='switch_active',
      help='Set new host as active host',
      action='store_true')
    
    # Create the parser for the "add" command
    parser_del = subparsers.add_parser(
      'delete',
      help="Delete a remote host",
      parents=[host_parent_parser])

    # Create the parser for the "switch" command
    parser_switch = subparsers.add_parser(
      'switch',
      help="Switch active remote host",
      parents=[host_parent_parser])

    # Create the parser for the "list" command
    parser_list = subparsers.add_parser(
      'list',
      help="List all remote hosts")
    parser_list.add_argument(
      "-v",
      "--verbose",
      dest="loglevel",
      help="set loglevel to INFO",
      action="store_const",
      const=logging.INFO)

    return parser.parse_args(args), parser


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    args_bk = args
    args, parser = parse_args(args)
    if len(args_bk) == 0:
      parser.print_help()
      parser.exit()

    setup_logging(args.loglevel)
    _logger.info("Starting loon...")
    host = Host()

    # Deparse arguments
    if args.subparsers_name == 'add':
      _logger.info("Add command is detected.")
      host.add(
        username=args.username,
        host=args.host,
        port=args.port)
      if args.switch_active:
        host.switch(
          username=args.username,
          host=args.host,
          port=args.port)
    elif args.subparsers_name == 'delete':
      _logger.info("Delete command is detected.")
      host.delete(
        username=args.username,
        host=args.host,
        port=args.port)
    elif args.subparsers_name == 'switch':
      _logger.info("Switch command is detected.")
      host.switch(
        username=args.username,
        host=args.host,
        port=args.port)
    elif args.subparsers_name == 'list':
      _logger.info("List command is detected.")
      host.list()


    _logger.info("loon ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
