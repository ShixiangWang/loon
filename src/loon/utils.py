import os
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
        raise ValueError("Input content must have the same number of columns as title")
    content.insert(0, title)

    table_t = list(map(list, zip(*content)))
    col_width = list(map(lambda x: max([len(str(i)) for i in x]), table_t))
    
    def print_mark_row(col_width):
        for i in col_width:
            print("+"+"-"*i, end="")
        print("+")
    
    print_mark_row(col_width)
    for row in content:
        for i, text in enumerate(row):
            print("|"+str(text)+" "*(col_width[i] - len(str(text))), end="")
        print("|")
        print_mark_row(col_width)

    return

if __name__ == "__main__":
    # Test pretty_table
    title = ['Alias', 'Username', 'IP address', 'Port']
    content = [['host1', 'wxx', '127.0.0.1', '22'],
                ['h2', 'asdfdsg', '134.23.41.34', '22']]
    pretty_table(title, content)

