# -*- coding: utf-8 -*-
import os

__version__ = "0.1.7"
__author__ = "ShixiangWang"
__copyright__ = "ShixiangWang"
__license__ = "mit"
# User can modify the following line
# to change the default path for host file
__host_file__ = "~/.config/loon/host.json"
# Get the absolute path for host file
# NEVER CHANGE IT!
__host_file__ = os.path.expanduser(__host_file__)
__privatekey_file__ = os.path.expanduser("~/.ssh/id_rsa")
