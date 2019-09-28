import os
from os.path import isfile, isdir

def create_parentdir(path):
    """Create parent directory for a file/directory if not exists"""
    dir = os.path.dirname(path)
    if not os.path.isdir(dir):
        os.makedirs(dir)

