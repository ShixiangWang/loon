# -*- coding: utf-8 -*-
"""
Tool functions
"""

import sys
from subprocess import run, PIPE
from loon.utils import isfile, isdir, read_csv


def batch(input, cmds, sep=',', header=False, dry_run=False, _logger=None):
    """Batch process commands according to mappings from file"""
    if not isfile(input):
        print("Error: file %s does not exist" % input)
        sys.exit(1)

    data = read_csv(input, sep=sep, rm_comment=True)
    if not header:
        # Remove header
        _ = data.pop(0)

    cmd_list = []
    for row in data:
        cmd_list.append(cmds.format(*row))
    for cmd in cmd_list:
        print("=> Running %s" % cmd)
        if not dry_run:
            run_res = run(cmd, shell=True)
            _logger.info("Status code: " + str(run_res.returncode))
            if run_res.returncode != 0:
                print("Error: some error occurred, please check the info!")
                sys.exit(run_res.returncode)

    return
