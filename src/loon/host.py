# -*- coding: utf-8 -*-
"""This is a class file for describing remote host"""

import argparse
import socket
import os
from ssh2.session import Session

# Reference:
# https://github.com/ParallelSSH/ssh2-python/tree/master/examples



USERNAME = "Administrator"

parser = argparse.ArgumentParser()

parser.add_argument('cmd', help="Command to run")
parser.add_argument('--host', dest='host',
                    default='localhost',
                    help='Host to connect to')
parser.add_argument('--port', dest='port', default=22,
                    help="Port to connect on", type=int)
parser.add_argument('-u', dest='user', default=USERNAME,
                    help="User name to authenticate as")


def main():
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))
    print("%s" %args.user)
    print("%s" %args.host)
    print("%s" %args.port)
    
    s = Session()
    s.handshake(sock)
    s.agent_auth(args.user)
    # session.userauth_publickey_fromfile(username, 'private_key_file')
    # session.userauth_password(username, '<my password>')
    chan = s.open_session()
    chan.execute(args.cmd)
    size, data = chan.read()
    while size > 0:
        print(data)
        size, data = chan.read()


if __name__ == "__main__":
    main()