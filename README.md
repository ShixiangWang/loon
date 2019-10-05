# loon - A Python toolkit for operating remote host based on SSH

![GitHub repo size](https://img.shields.io/github/repo-size/ShixiangWang/loon) [![PyPI](https://img.shields.io/pypi/v/loon?color=blue)](https://pypi.org/project/loon/) [![Documentation Status](https://readthedocs.org/projects/loon/badge/?version=latest)](https://loon.readthedocs.io/en/latest/?badge=latest) ![PyPI - Downloads](https://img.shields.io/pypi/dm/loon) [![GitHub issues](https://img.shields.io/github/issues-raw/ShixiangWang/loon)](https://github.com/ShixiangWang/loon/issues?q=is%3Aopen+is%3Aissue) [![GitHub last commit](https://img.shields.io/github/last-commit/ShixiangWang/loon)](https://github.com/ShixiangWang/loon/commits/master) 


## Description

Idea for developing **loon** comes from [sync-deploy](https://github.com/ShixiangWang/sync-deploy), which help me run commands, copy and download files on/to/from remote host. This toolkit is built on the top of [ssh2-python library](https://github.com/ParallelSSH/ssh2-python).

## Installation

Install from pypi:

```bash
pip install loon
```

## Usage

### Configuration

To access remote host without typing password, you have to generate ssh key with `ssh-keygen` command if it is not available.

```shell
$ ssh-keygen
```

Follow the commands, for simplicity, just type `ENTER` to proceed.

Copy your key to remote server, replace `user` with your `username` and `host` with your remote host ip address.

```shell
$ ssh-copy-id -i ~/.ssh/id_rsa user@host
```

### Host management

- Add a remote host

```shell
$ loon add -U wsx -H 127.0.0.1 -P 22
=> Added successfully!
# Default port is 22, so don't need to specify it
# And we can create a host alias, otherwise
# it is same as username of remote host
$ loon add -U wsx -H 127.0.0.2 -N host2      
=> Added successfully!
```

- List all remote hosts

```shell
$ loon list
+-----+--------+----------+----+
|Alias|Username|IP address|Port|
+-----+--------+----------+----+
|<wsx>|wsx     |127.0.0.1 |22  |
+-----+--------+----------+----+
|host2|wsx     |127.0.0.2 |22  |
+-----+--------+----------+----+
<active host>
```

- Rename alias

```shell
$ loon rename wsx host1
$ loon list
+-------+--------+----------+----+
|Alias  |Username|IP address|Port|
+-------+--------+----------+----+
|<host1>|wsx     |127.0.0.1 |22  |
+-------+--------+----------+----+
|host2  |wsx     |127.0.0.2 |22  |
+-------+--------+----------+----+
<active host>
```

- Switch active remote host

```shell
$ loon switch -N host2
=> Activated.
$ loon list
+-------+--------+----------+----+
|Alias  |Username|IP address|Port|
+-------+--------+----------+----+
|host1  |wsx     |127.0.0.1 |22  |
+-------+--------+----------+----+
|<host2>|wsx     |127.0.0.2 |22  |
+-------+--------+----------+----+
<active host>
```

- Delete a host

```shell
$ loon delete -N host2
=> Removing host from available list...
=> Removing active host...
=> Changing active host to host1
$ loon list
+-------+--------+----------+----+
|Alias  |Username|IP address|Port|
+-------+--------+----------+----+
|<host1>|wsx     |127.0.0.1 |22  |
+-------+--------+----------+----+
<active host>
```

### Common tasks

- Run commands

```shell
$ loon run 'ls -l ~'
total 168
drwxr-xr-x     2 wsx liulab     25 Apr  7 23:26 bin
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Desktop
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Documents
drwxr-xr-x.    3 wsx liulab     69 Jun 10 16:57 Downloads
drwxr-xr-x     2 wsx liulab      6 Sep 30 10:23 facet
drwxr-xr-x    11 wsx liulab   4096 Sep 22 20:13 metawho
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Music
drwxr-xr-x     3 wsx liulab     60 Apr 30 17:50 Notebooks
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Pictures
drwxr-xr-x     6 wsx liulab    114 Sep 27 17:33 projects
drwxr-xr-x     6 wsx liulab     96 Jun 27 16:50 projects_bk
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Public
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Templates
drwxr-xr-x     5 wsx liulab   4096 Oct  3 12:24 test
drwxr-xr-x  3480 wsx liulab 114688 Oct  3 13:44 tmp
drwxr-xr-x     3 wsx liulab     32 Aug 22 17:13 tools
drwxr-xr-x.    2 wsx liulab      6 Apr  4 10:36 Videos
```

- Upload files (not fully supported)

TODO

### PBS management and tasks

TODO

### Current usage info

```shell
usage: loon [-h] [--version] [--author]
            {add,delete,switch,list,rename,run,upload} ...

Be an efficient loon.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --author              show info of program's author

subcommands:
  {add,delete,switch,list,rename,run,upload}
                        description
    add                 Add a remote host
    delete              Delete a remote host
    switch              Switch active remote host
    list                List all remote hosts
    rename              Rename host alias
    run                 Run commands on the active remote host
    upload              Upload files to active remote host
```

## Note

This project has been set up using PyScaffold 3.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
