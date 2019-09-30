# -*- coding: utf-8 -*-
"""Classes used in loon package"""

import json
import pprint
from loon.skeleton import __host_file__
from loon.utils import create_parentdir, isfile, isdir

class Host:
    """
    Representation of remote host
    """
    def __init__(self, hostfile = __host_file__):
        self.hostfile = hostfile
        self.load_hosts()
        return

    def load_hosts(self):
        """Load hosts from file"""
        if not isfile(self.hostfile):
            self.active_host = []
            self.available_hosts = []
        else:
            with open(self.hostfile, 'r') as f:
                hosts = json.load(f)
            self.active_host = hosts['active']
            self.available_hosts = hosts['available']
        return

    def save_hosts(self):
        """Save hosts to file"""
        # if len(self.active_host)==0 or len(self.available_hosts)==0:
        #     raise ValueError("Cannot save to file due to null host.")
        hosts = {'active':self.active_host, 'available':self.available_hosts}
        if not isfile(self.hostfile):
            # Create parent dir if hostfile does not exist
            create_parentdir(self.hostfile)
        with open(self.hostfile, 'w') as f:
            json.dump(hosts, f)
        return

    def add(self, username, host, port=22):
        """Add a remote host"""
        info = [username, host, port]

        if info in self.available_hosts:
            print("=> Input host exists. Will not change.")
            return
        else:
            self.available_hosts.append(info)
            if len(self.active_host) == 0:
                self.active_host = info
            self.save_hosts()
            print("=> Added successfully!")
        return

    def delete(self, username, host, port=22):
        """Delete a remote host"""
        info = [username, host, port]
        if info in self.available_hosts:
            print("=> Removing host from available list...")
            self.available_hosts.remove(info)
            if info == self.active_host:
                print("=> Removing active host...")
                if len(self.available_hosts) > 0:
                    self.active_host = self.available_hosts[0]
                    print("=> Changing active host to %s" %self.active_host)
                else:
                    self.active_host = []  # reset
                    print("=> Reseting active host to []")
            self.save_hosts()
            print("=> Deleted.")
        else:
            print("=> Host does not exist, please check input with hostlist command!")
        return
    
    def switch(self, username, host, port=22):
        """Switch active host"""
        info = [username, host, port]
        if info in self.available_hosts:
            self.active_host = info
            self.save_hosts()
            print("=> Done.")
        else:
            print("Host does not exist, please check input with hostlist command!")
        return
        
    def list(self):
        """List all remote hosts"""
        pp = pprint.PrettyPrinter(width=40)
        print()
        print("Active host")
        print("="*12)
        print("%s" %self.active_host)
        print()
        print("Available hosts")
        print("="*15)
        pp.pprint(self.available_hosts)
        return
    
    def connect(self):
        """Connect active host"""
        pass
    
    def cmd(self):
        """Run command(s) in active remote host"""
        pass

    def upload(self):
        """Upload files to active remote host"""
        pass
    def download(self):
        """Download files to local machine from active remote host"""
        pass


class PBS:
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

if __name__ == "__main__":
    host = Host()
    host.add(username="wangshx", host="127.0.0.1")
    host.add(username="wsx", host="127.0.0.1", port=21)
    host.add(username="zzz", host="127.0.0.1")
    host.list()
    host.delete(username="zzz", host="127.0.0.1")
    host.switch(username="wangshx", host="127.0.0.1")
    #host.delete(username="127.0.0.1", host="127.0.0.1")
    host.list()
