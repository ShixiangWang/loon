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

if __package__ == '' or __package__ is None:    # Use for test
    from __init__ import __version__, __author__, __license__
    from classes import Host, PBS
    from tool import batch
else:
    from loon import __version__, __author__, __license__
    from loon.classes import Host, PBS
    from loon.tool import batch

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Be an efficient loon.")

    # Show version info
    parser.add_argument(
        "--version",
        action="version",
        version="loon {ver} released under {license} license.".format(
            ver=__version__, license=__license__.upper()))
    parser.add_argument(
        "--author",
        action="version",
        help="show info of program's author",
        version="Author: 王诗翔 Email: w_shixiang@163.com GitHub: @{author}".
        format(author=__author__))

    # Common arguments
    host_parent_parser = argparse.ArgumentParser(add_help=False)
    host_parent_parser.add_argument(
        '-N',
        '--name',
        dest="name",
        help='Host alias, default is value from -U',
        type=str)
    host_parent_parser.add_argument('-U',
                                    '--username',
                                    dest='username',
                                    help='Username for remote host',
                                    type=str)
    host_parent_parser.add_argument(
        '-H',
        '--host',
        dest='host',
        help='IP address for remote host (e.g. 192.168.0.1)',
        type=str)
    host_parent_parser.add_argument('-P',
                                    '--port',
                                    dest="port",
                                    help='Port for remote host, default is 22',
                                    type=int,
                                    default=22)

    verbose_parser = argparse.ArgumentParser(add_help=False)
    verbose_parser.add_argument("-v",
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
        parents=[host_parent_parser, verbose_parser])
    parser_add.add_argument('-A',
                            '--active',
                            dest='switch_active',
                            help='Set new host as active host',
                            action='store_true')

    # Create the parser for the "add" command
    parser_del = subparsers.add_parser(
        'delete',
        help="Delete a remote host",
        parents=[host_parent_parser, verbose_parser])

    # Create the parser for the "switch" command
    parser_switch = subparsers.add_parser(
        'switch',
        help="Switch active remote host",
        parents=[host_parent_parser, verbose_parser])

    # Create the parser for the "list" command
    parser_list = subparsers.add_parser('list',
                                        help="List all remote hosts",
                                        parents=[verbose_parser])

    # Create the parser for the "rename" command
    parser_rename = subparsers.add_parser('rename',
                                          help="Rename host alias",
                                          parents=[verbose_parser])
    parser_rename.add_argument('old', help="Old host alias", type=str)
    parser_rename.add_argument('new', help="New host alias", type=str)

    # Create the parser for the "run" command
    parser_run = subparsers.add_parser(
        'run',
        help='Run commands or scripts on remote',
        parents=[verbose_parser])
    parser_run.add_argument(
        nargs='+',
        dest='commands',
        help=
        "Commands/scripts to run, special symbol or option should be quoted, e.g. 'ls -l ~', 'ls -l'"
    )
    parser_run.add_argument('-f',
                            '--file',
                            dest='run_file',
                            help='Run scripts instead of commands',
                            action='store_true')
    parser_run.add_argument(
        '--data',
        help=('Include a data directory when run local scripts'),
        type=str,
        required=False)
    parser_run.add_argument(
        '--remote',
        dest='remote_file',
        help='Scripts are directly from the active remote host',
        action='store_true')
    parser_run.add_argument(
        '--dir',
        help=
        'Remote directory for storing local scripts. Only used when flag --file sets and --remote does not set. Default is /tmp',
        default='/tmp')
    parser_run.add_argument(
        '--prog',
        help=
        'Specified program to run scripts, if not set, scripts will be executed directly assuming shbang exist',
        required=False)

    # Create the parser for the "upload" command
    parser_upload = subparsers.add_parser(
        'upload',
        help='Upload files to active remote host',
        parents=[verbose_parser])
    parser_upload.add_argument('source',
                               nargs='+',
                               help='Source files to upload')
    parser_upload.add_argument('destination',
                               help="Remote destination directory",
                               type=str)
    parser_upload.add_argument('--rsync',
                               help="Use rsync instead of scp",
                               action='store_true')

    # Create the parser for the "download" command
    parser_download = subparsers.add_parser(
        'download',
        help='Download files from active remote host',
        parents=[verbose_parser])
    parser_download.add_argument('source',
                                 nargs='+',
                                 help='Source files to download')
    parser_download.add_argument(
        'destination',
        help=
        "Local destination directory, note '~' should be quoted in some cases",
        type=str)
    parser_download.add_argument('--rsync',
                                 help="Use rsync instead of scp",
                                 action='store_true')

    # Create the parser for the "gen" command
    parser_gen = subparsers.add_parser(
        'gen',
        help='Generate a batch of (script) files',
        parents=[verbose_parser])
    parser_gen.add_argument('-t',
                            '--template',
                            help="A template file containing placeholders")
    parser_gen.add_argument(
        '-s',
        '--samplefile',
        help=
        "A csv file containing unique filenames (the first column) and replacing labels"
    )
    parser_gen.add_argument(
        '-m',
        '--mapfile',
        help=
        "A csv file containing placeholders and column index (0-based) indicating replacing labels in samplefile"
    )
    parser_gen.add_argument('-o', '--output', help="Output directory")

    # Create the parser for the "batch" command
    parser_batch = subparsers.add_parser(
        'batch',
        help="Batch process commands with placeholders",
        parents=[verbose_parser])
    parser_batch.add_argument(
        '-f',
        '--file',
        help=
        r'A structed file like CSV, TSV etc. Each column is placeholder target, i.e. {0} targets the first column, {1} targets the second column, etc.',
        type=str,
        required=True)
    parser_batch.add_argument(
        '-s',
        '--sep',
        help=r"File separator, ',' for CSV (default) and '\t' for TSV",
        default=',',
        required=False)
    parser_batch.add_argument('-T',
                              '--thread',
                              help="Thread number, default is 1",
                              required=False,
                              default=1,
                              type=int)
    parser_batch.add_argument('--header',
                              help="Set it if input file contains header",
                              action='store_true')
    parser_batch.add_argument('--dry',
                              help="Dry run the commands",
                              action='store_true')
    parser_batch.add_argument('cmds',
                              type=str,
                              help="A sample command with placeholders")

    # Create the parser for the "pbstemp" command
    parser_pbstemp = subparsers.add_parser('pbstemp',
                                           help='Generate a PBS template file',
                                           parents=[verbose_parser])
    parser_pbstemp.add_argument(
        '-i',
        '--input',
        help='A template file, if not set, a default template is used',
        type=str,
        required=False)
    parser_pbstemp.add_argument('-o',
                                '--output',
                                help="Output file, default is work.pbs",
                                type=str,
                                required=False)

    # Create the parser for the "pbsgen" command
    parser_pbsgen = subparsers.add_parser(
        'pbsgen',
        help='Generate a batch of PBS files (with .pbs extension)',
        parents=[verbose_parser])
    parser_pbsgen.add_argument(
        '-t', '--template', help="A PBS template file containing placeholders")
    parser_pbsgen.add_argument(
        '-s',
        '--samplefile',
        help=
        "A csv file containing unique filenames (the first column) and replacing labels"
    )
    parser_pbsgen.add_argument(
        '-m',
        '--mapfile',
        help=
        "A csv file containing placeholders and column index (0-based) indicating replacing labels in samplefile"
    )
    parser_pbsgen.add_argument('-o', '--output', help="Output directory")

    # Create the parser for the "pbsgen_example" command
    parser_genexample = subparsers.add_parser(
        'pbsgen_example',
        help='Generate example files for pbsgen command',
        parents=[verbose_parser])
    parser_genexample.add_argument('output', help='Output directory')

    # Create the parser for the "pbssub" command
    parser_pbssub = subparsers.add_parser('pbssub',
                                          help='Submit PBS tasks',
                                          parents=[verbose_parser])
    parser_pbssub.add_argument(
        '--remote',
        dest='remote_file',
        help='PBS task files are located at the active remote host',
        action='store_true')
    parser_pbssub.add_argument(
        '--workdir',
        help=
        'Working directory, default is /tmp for remote host and otherwise the command executed path',
        required=False)
    parser_pbssub.add_argument(
        nargs='+',
        dest='tasks',
        help="Tasks to submit, can be a directory containing only PBS files")

    # Create the parser for the "pbsdeploy" command
    parser_deploy = subparsers.add_parser(
        'pbsdeploy',
        help='Deploy target destination to remote host',
        parents=[verbose_parser])
    parser_deploy.add_argument(
        'target', help='Target directory containing PBS files and more')
    parser_deploy.add_argument(
        'destination',
        help=
        "Local destination directory, note '~' should be quoted in some cases",
        nargs='?')
    parser_deploy.add_argument('--rsync',
                               help="Use rsync instead of scp",
                               action='store_true')

    # Create the parser for the "pbscheck" command
    parser_pbscheck = subparsers.add_parser(
        'pbscheck',
        help='Check status of PBS job on remote host',
        parents=[verbose_parser])
    parser_pbscheck.add_argument(
        'job_id',
        help="ID of job, if not set, all running jobs will be returned",
        type=str,
        nargs='?')

    return parser.parse_args(args), parser


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel,
                        stream=sys.stdout,
                        format=logformat,
                        datefmt="%Y-%m-%d %H:%M:%S")


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
    pbs = PBS()

    if hasattr(args, 'rsync') and args.rsync:
        use_rsync = True
    else:
        use_rsync = False

    # Deparse arguments
    if args.subparsers_name == 'add':
        _logger.info("Add command is detected.")
        if args.username is None or args.host is None:
            print("Error: username and host are both required in add command.")
            sys.exit(1)
        if args.name is None:
            args.name = args.username
        host.add(name=args.name,
                 username=args.username,
                 host=args.host,
                 port=args.port)
        if args.switch_active:
            host.switch(name=args.name,
                        username=args.username,
                        host=args.host,
                        port=args.port)
    elif args.subparsers_name == 'delete':
        _logger.info("Delete command is detected.")
        if args.username is None or args.host is None:
            if args.name is None:
                print("Error: either specify name or both username and host")
                sys.exit(1)
        host.delete(name=args.name,
                    username=args.username,
                    host=args.host,
                    port=args.port)
    elif args.subparsers_name == 'switch':
        _logger.info("Switch command is detected.")
        if args.username is None or args.host is None:
            if args.name is None:
                print("Error: either specify name or both username and host")
                sys.exit(1)
        host.switch(name=args.name,
                    username=args.username,
                    host=args.host,
                    port=args.port)
    elif args.subparsers_name == 'list':
        _logger.info("List command is detected.")
        host.list()
    elif args.subparsers_name == 'rename':
        _logger.info("Rename command is detected.")
        host.rename(args.old, args.new)
    elif args.subparsers_name == 'run':
        _logger.info("Run command is detected.")
        if args.run_file:
            commands = args.commands
        else:
            commands = " ".join(args.commands)
        host.cmd(commands,
                 _logger=_logger,
                 run_file=args.run_file,
                 data_dir=args.data,
                 remote_file=args.remote_file,
                 dir=args.dir,
                 prog=args.prog)
    elif args.subparsers_name == 'upload':
        _logger.info("Upload command is detected.")
        #host.connect(open_channel=False)
        host.upload(args.source,
                    args.destination,
                    _logger=_logger,
                    use_rsync=use_rsync)
    elif args.subparsers_name == 'download':
        _logger.info("Download command is detected.")
        #host.connect(open_channel=False)
        host.download(args.source,
                      args.destination,
                      _logger=_logger,
                      use_rsync=use_rsync)
    elif args.subparsers_name == 'batch':
        _logger.info("Batch command is detected.")
        batch(args.file,
              args.cmds,
              sep=args.sep,
              thread=args.thread,
              header=args.header,
              dry_run=args.dry,
              _logger=_logger)
    elif args.subparsers_name == 'pbstemp':
        _logger.info("pbstemp command is detected.")
        pbs.gen_template(args.input, args.output)
    elif args.subparsers_name == 'gen':
        _logger.info("gen command is detected.")
        pbs.gen_pbs(args.template,
                    args.samplefile,
                    args.mapfile,
                    args.output,
                    _logger=_logger,
                    pbs_mode=False)
    elif args.subparsers_name == 'pbsgen':
        _logger.info("pbsgen command is detected.")
        pbs.gen_pbs(args.template,
                    args.samplefile,
                    args.mapfile,
                    args.output,
                    _logger=_logger)
    elif args.subparsers_name == 'pbsgen_example':
        pbs.gen_pbs_example(args.output, _logger=_logger)
    elif args.subparsers_name == 'pbssub':
        _logger.info("pbssub command is detected.")
        pbs.sub(host,
                args.tasks,
                args.remote_file,
                args.workdir,
                _logger=_logger)
    elif args.subparsers_name == 'pbsdeploy':
        _logger.info("pbsdeploy command is detected.")
        pbs.deploy(host,
                   args.target,
                   args.destination,
                   _logger=_logger,
                   use_rsync=use_rsync)
    elif args.subparsers_name == 'pbscheck':
        _logger.info("pbscheck command is detected.")
        pbs.check(host, args.job_id)

    _logger.info("loon ends here")


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
