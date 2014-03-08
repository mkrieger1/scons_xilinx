import os

def get_suffix(filename):
    return os.path.splitext(str(filename))[1]

def replace_suffix(filename, suffix):
    return os.path.splitext(str(filename))[0]+suffix

def replace_path(filename, path):
    return os.path.join(path, os.path.basename(str(filename)))

