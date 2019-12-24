# -*- coding: utf-8 -*-
"""
Tool functions
"""

import sys
import io
import re
from subprocess import run
from multiprocessing import Pool
from loon.utils import isfile, isdir, read_csv


def prun(x):
    y = run(x, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return y


def batch(input,
          cmds,
          sep=',',
          header=False,
          thread=1,
          dry_run=False,
          _logger=None):
    """Batch process commands according to mappings from file
    
    Args:
        input: stdin or a path to input file
        cmds: template command (with placeholder) to run
        sep: separator, default is ','
        header: set `True` if input data contains a header line
        thread: number of threads to run in parallel
        dry_run: if `True`, dry run the code
        _logger: the logging logger

    Returns:
        None
    """
    # if not isfile(input):
    #     print("Error: file %s does not exist" % input)
    #     sys.exit(1)

    if isinstance(input, io.TextIOWrapper):
        data = []
        for row in input.readlines():
            data.append(row.strip().split(sep=sep))
    else:
        data = read_csv(input, sep=sep, rm_comment=True)

    if header:
        if re.compile(r'{\d+}').search(cmds) is not None:
            # Remove header
            _ = data.pop(0)
        elif re.compile(r'{.+}').search(cmds) is not None:
            colnames = data.pop(0)
            for index, name in enumerate(colnames):
                pattern = "{{{}}}".format(name)
                sub = "{{{}}}".format(index)
                if re.compile(pattern).search(cmds) is not None:
                    cmds = cmds.replace(pattern, sub)
        else:
            print(
                "Please set correct placeholders either with {numeric} or {column_names} format!",
                file=sys.stderr)
            sys.exit(1)

    cmd_list = []
    for row in data:
        try:
            cmd_list.append(cmds.format(*row))
        except IndexError:
            print(r"Error: bad placeholder, valid is {0} to {%s}" %
                  (str(len(row) - 1)),
                  file=sys.stderr)
            sys.exit(1)
        except KeyError:
            print("Error: bad placeholder, valid are",
                  colnames,
                  file=sys.stderr)
            sys.exit(1)

    if dry_run:
        _ = [print("=> Running %s" % cmd) for cmd in cmd_list]
        sys.exit(0)

    # There is a bug when input from stdin I cannot figure out for now
    if thread > 1:
        _logger.info("Using %s threads" % str(thread))
        with Pool(processes=thread) as p:
            if isinstance(input, io.TextIOWrapper):
                p.map(prun, cmd_list)
                sys.exit(0)
            else:
                run_res = p.map(prun, cmd_list)
                for _, res in enumerate(run_res):
                    if res.returncode != 0:
                        print("Error: some jobs failed, please take a check!.",
                              file=sys.stderr)
                        sys.exit(res.returncode)
    else:
        _logger.info("Using %s threads" % str(thread))
        for cmd in cmd_list:
            if isinstance(input, io.TextIOWrapper):
                run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
            else:
                run_res = run(cmd,
                              shell=True,
                              stdout=sys.stdout,
                              stderr=sys.stderr)
                _logger.info("Status code: " + str(run_res.returncode))
                if run_res.returncode != 0:
                    print(
                        "Error: an error detected when running the following command, please take a check!",
                        file=sys.stderr)
                    print("\t", cmd, file=sys.stderr)
                    print("Status code: %s" % str(run_res.returncode),
                          file=sys.stderr)
                    print(
                        "Please don't run with --verbose, there is a known issue with it.",
                        file=sys.stderr)
                    sys.exit(run_res.returncode)
        sys.exit(0)

    return
