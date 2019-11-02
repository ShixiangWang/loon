# -*- coding: utf-8 -*-
"""
Tool functions
"""

import sys
from subprocess import run
from multiprocessing import Pool
from loon.utils import isfile, isdir, read_csv


def prun(x):
    y = run(x, shell=True)
    return y


def batch(input,
          cmds,
          sep=',',
          header=False,
          thread=1,
          dry_run=False,
          _logger=None):
    """Batch process commands according to mappings from file"""
    if not isfile(input):
        print("Error: file %s does not exist" % input)
        sys.exit(1)

    data = read_csv(input, sep=sep, rm_comment=True)
    if header:
        # Remove header
        _ = data.pop(0)

    cmd_list = []
    for row in data:
        try:
            cmd_list.append(cmds.format(*row))
        except IndexError:
            print(r"Error: bad placeholder, valid is {0} to {%s}" %
                  (str(len(row) - 1)))
            sys.exit(1)

    if dry_run:
        _ = [print("=> Running %s" % cmd) for cmd in cmd_list]
        sys.exit(0)

    if thread > 1:
        _logger.info("Using %s threads" % str(thread))
        with Pool(thread) as p:
            run_res = p.map(prun, cmd_list)
        for index, res in enumerate(run_res):
            _logger.info("Status code: " + str(res.returncode))
            if res.returncode != 0:
                print("Error: job %s failed, please check the info!." %
                      str(index))
    else:
        for cmd in cmd_list:
            run_res = run(cmd, shell=True)
            _logger.info("Status code: " + str(run_res.returncode))
            if run_res.returncode != 0:
                print("Error: some error occurred, please check the info!")
                sys.exit(run_res.returncode)

    return
