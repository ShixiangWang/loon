# loon - A Python toolkit for operating remote host

![GitHub repo size](https://img.shields.io/github/repo-size/ShixiangWang/loon) [![PyPI](https://img.shields.io/pypi/v/loon?color=blue)](https://pypi.org/project/loon/) [![Documentation Status](https://readthedocs.org/projects/loon/badge/?version=latest)](https://loon.readthedocs.io/en/latest/?badge=latest) ![PyPI - Downloads](https://img.shields.io/pypi/dm/loon) [![GitHub issues](https://img.shields.io/github/issues-raw/ShixiangWang/loon)](https://github.com/ShixiangWang/loon/issues?q=is%3Aopen+is%3Aissue) [![GitHub last commit](https://img.shields.io/github/last-commit/ShixiangWang/loon)](https://github.com/ShixiangWang/loon/commits/master) 


## Description

**loon** is a Python toolkit for operating remote host based on SSH. Idea for developing **loon** comes from [**sync-deploy**](https://github.com/ShixiangWang/sync-deploy), which is limited by its pure bash code. Therefore, I use Python to implement it and more features will be added to it in the future. 

**For Windows users, software providing basic linux commands like `ssh` and `scp` is required, I recommend using [git bash](https://git-scm.com/downloads).**

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

- Run local scripts

This will upload scripts to remote host firstly, then run them.

```shell
$ loon run -f ../../tests/scripts/t*.py
=> Starting upload...

t1.py                                          100%   50    49.0KB/s   00:00    
t2.py                                          100%   50    77.6KB/s   00:00    

=> Finished uploading in 1s
=> Getting results:
This is t1 script.
This is t2 script.
```

- If input contains both files and directories, all files in directory will not be executed. This is a way to include child scripts which does not need to be executed. 
- If input is only a directory, all scripts (not including scripts in subdirectories) under it will be executed. This is the way to maintain an independent project.

You can include data directory using `--data` flag, specify program like `bash` or `python` using `--prog` flag and set remote directory using `--dir` flag.

- Upload and download files 

Use them like `cp` command.

```shell
$ loon upload -h
usage: loon upload [-h] [-v] source [source ...] destination

positional arguments:
  source         Source files to upload
  destination    Remote destination directory, note '~' should be quoted in
                 some cases

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  set loglevel to INFO

$ loon download -h
usage: loon download [-h] [-v] source [source ...] destination

positional arguments:
  source         Source files to download
  destination    Local destination directory, note '~' should be quoted in
                 some cases

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  set loglevel to INFO
```

### PBS management and tasks

- Added `pbstemp` command
- Added `pbscheck` command

TODO

### Current usage info

```shell
usage: loon [-h] [--version] [--author]
                   {add,delete,switch,list,rename,run,upload,download,pbstemp,pbscheck}
                   ...

Be an efficient loon.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --author              show info of program's author

subcommands:
  {add,delete,switch,list,rename,run,upload,download,pbstemp,pbscheck}
                        description
    add                 Add a remote host
    delete              Delete a remote host
    switch              Switch active remote host
    list                List all remote hosts
    rename              Rename host alias
    run                 Run commands or scripts on the active remote host
    upload              Upload files to active remote host
    download            Download files from active remote host
    pbstemp             Generate a PBS template file
    pbscheck            Check status of a PBS job on remote host
```

## Note

This project has been set up using PyScaffold 3.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
