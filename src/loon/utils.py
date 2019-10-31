import os
import csv
from os.path import isfile, isdir


def create_parentdir(path):
    """Create parent directory for a file/directory if not exists
    
    Args:
        path ([str]): a file path
    """
    dir = os.path.dirname(path)
    if not os.path.isdir(dir):
        os.makedirs(dir)


def pretty_table(title, content):
    """Print a pretty table according to the title and content
    
    Args:
        title ([str]): a list containing the title of table, e.g. ['title1', 'title2']
        content ([str]): a nested list containing the content of table, e.g. [['a1', 'a2'], ['b1', 'b2']]
    """
    title_ncol = len(title)
    content_ncols = map(len, content)
    if not all([title_ncol == i for i in content_ncols]):
        raise ValueError(
            "Input content must have the same number of columns as title")
    content.insert(0, title)

    table_t = list(map(list, zip(*content)))
    col_width = list(map(lambda x: max([len(str(i)) for i in x]), table_t))

    def print_mark_row(col_width):
        for i in col_width:
            print("+" + "-" * i, end="")
        print("+")

    print_mark_row(col_width)
    for row in content:
        for i, text in enumerate(row):
            print("|" + str(text) + " " * (col_width[i] - len(str(text))),
                  end="")
        print("|")
        print_mark_row(col_width)

    return


def get_filelist(dirName):
    """Create a list of file and sub directories names in the given directory.
    
    Source code from: https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    """
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if isdir(fullPath):
            allFiles = allFiles + get_filelist(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw:
            yield raw


def read_csv(file_path, sep=',', rm_comment=True):
    """Read CSV file"""
    res = []
    with open(file_path, "r", encoding='utf-8') as f:
        if rm_comment:
            csv_reader = csv.reader(decomment(f), delimiter=sep)
        else:
            csv_reader = csv.reader(f, delimiter=sep)
        for row in csv_reader:
            res.append(row)
    return res


if __name__ == "__main__":
    # Test pretty_table
    title = ['Alias', 'Username', 'IP address', 'Port']
    content = [['host1', 'wxx', '127.0.0.1', '22'],
               ['h2', 'asdfdsg', '134.23.41.34', '22']]
    pretty_table(title, content)
