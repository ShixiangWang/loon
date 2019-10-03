# -*- coding: utf-8 -*-
"""Classes used in loon package"""

import sys
import os
import json
import pprint
import socket
from datetime import datetime
from ssh2.session import Session
if __package__ == '' or __package__ is None:  # Use for test
    from __init__ import __host_file__
    from utils import create_parentdir, isfile, isdir
else:
    from loon import __host_file__
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

        if any(isinstance(i, list) for i in self.active_host):
            print("Error: more than one active host. Please check config file ~/.config/loon/host.json and modify or remove it if necessary.")

        # Python code to remove duplicate elements 
        def RemoveDups(duplicate): 
            final_list = [] 
            flag = False
            for num in duplicate: 
                if num not in final_list: 
                    final_list.append(num) 
                else: 
                    flag = True
            return final_list, flag
        
        self.available_hosts, flag = RemoveDups(self.available_hosts)
        
        if flag:
            # Save unique hosts immediately
            self.save_hosts()

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

    def add(self, name, username, host, port=22):
        """Add a remote host"""
        info = [name, username, host, port]

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

    def host_check(self, name, username, host, port=22):
        host = []
        if name is not None:
            for h in self.available_hosts:
                if h[0] == name:
                    host = h.copy()
        else:
            info = [username, host, port]
            for h in self.available_hosts:
                if h[1:] == info:
                    host = h.copy()
        if len(host) == 0:
            print("=> Host does not exist, please check input with list command!")
            sys.exit(1)
        return host

    def delete(self, name, username, host, port=22):
        """Delete a remote host"""
        host2del = self.host_check(name, username, host, port)
        print("=> Removing host from available list...")
        self.available_hosts.remove(host2del)
        if host2del == self.active_host:
            print("=> Removing active host...")
            if len(self.available_hosts) > 0:
                self.active_host = self.available_hosts[0]
                print("=> Changing active host to %s" %self.active_host[0])
            else:
                self.active_host = []  # reset
                print("=> Reseting active host to []")
        self.save_hosts()
        return
    
    def switch(self, name, username, host, port=22):
        """Switch active host"""
        host2switch = self.host_check(name, username, host, port)
        self.active_host = host2switch
        self.save_hosts()
        print("=> Activated.")
        return

    def rename(self, old, new):
        """Rename host name"""
        host2rename = []        
        for index, h in enumerate(self.available_hosts):
            if h[0] == old:
                host2rename = h.copy()
                self.available_hosts[index][0] = new
        if len(host2rename) == 0:
            print("=> Host does not exist, please check input with list command!")
            sys.exit(1)
        if host2rename == self.active_host:
            self.active_host[0] = new
        self.save_hosts()
        return
        
        
    def list(self):
        """List all remote hosts"""

        #TODO Create a pretty table for showing list
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
    
    def connect(self, privatekey_file="~/.ssh/id_rsa", passphrase='', open_channel=True):
        """Connect active host and open a session"""
        privatekey_file = os.path.expanduser(privatekey_file)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.active_host[2], self.active_host[3]))
        s = Session()
        s.handshake(sock)
        try:
            # Try using private key file first
            s.userauth_publickey_fromfile(self.active_host[1], privatekey_file, passphrase)
        except:
            # Use password to auth
            passwd = input('No private key found.\nEnter your password for %s: ' %self.active_host[1])
            s.userauth_password(self.active_host[1], passwd)
        self.session = s
        if open_channel:
            self.channel = self.session.open_session()
        return
    
    def cmd(self, commands):
        """Run command(s) in active remote host using channel session
        Therefore, `open_channel` in `connect` method must be `True` before using it.

        Args:
            commands ([str]): commands run on active remote host
        """
        self.connect()
        self.channel.execute(commands)

        size, errinfo = self.channel.read_stderr()
        if size > 0:
            print('An error is raised by remote host, please read the info:\n')
            print(errinfo.decode('utf-8'), end="")
            sys.exit(1)
        else:
            # Get output
            datalist = []
            size, data = self.channel.read()
            # Here data is byte type
            while size > 0:
                data = data.decode('utf-8')
                print(data, end='')
                datalist.append(data)
                size, data = self.channel.read()
        
        # Return a list containing output from commands 
        return datalist

    def upload(self, source, destination):
        """Upload files to active remote host
        Args:
            source [(list)]: list of files (directories) to remote host
            destination [(str)]: destination directory
        """
        print("Starting upload...")
        now = datetime.now()
        for i in source:
            info = os.stat(i)
            print("Uploading %s to %s" %(i, destination))
            destination = '/'.join([destination, os.path.basename(i)])
            chan = self.session.scp_send64(
                destination,
                info.st_mode & 0o777,
                info.st_size,
                info.st_mtime,
                info.st_atime
            )
            with open(i, 'rb') as local_fh:
                for data in local_fh:
                    chan.write(data)
        taken = datetime.now() - now
        print("Finished uploading in %s" %taken)
        return
     
        
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
    host.add(username="wsx", host="10.19.24.165")
    host.list()
    host.cmd("ls -l")
