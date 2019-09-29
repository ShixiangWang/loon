# -*- coding: utf-8 -*-
"""Classes used in loon package"""

from loon import __host_file__

class host:
    """
    Representation of remote host
    """
    def __init__(self, hostfile = __host_file__):
        self.hostfile = hostfile
    def add(self):
        """Add a remote host"""
        pass
    def delete(self):
        """Delete a remote host"""
        pass
    def list(self):
        """List all remote hosts"""
        pass
    def switch(self):
        """Switch active host"""
        pass
    def upload(self):
        """Upload files to active remote host"""
        pass
    def download(self):
        """Download files to local machine from active remote host"""
        pass
    def cmd(self):
        """Run command(s) in active remote host"""
        pass

class pbs:
    """
    Representation of PBS task
    """
    def __init__(self):
        pass
    def gen_template(self):
        pass
    def gen_pbs(self):
        pass
    def sub(self):
        """Submit all pbs tasks in a remote directory"""
        pass
    def check(self):
        """Check PBS task status"""
        pass
