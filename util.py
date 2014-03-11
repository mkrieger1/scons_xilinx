import os
from fnmatch import fnmatch

def get_suffix(filename):
    return os.path.splitext(str(filename))[1]

def replace_suffix(filename, suffix):
    return os.path.splitext(str(filename))[0]+suffix

def replace_path(filename, path):
    return os.path.join(path, os.path.basename(str(filename)))

def get_file_list(path, pattern):
    """Return filenames from `path` that match `pattern`.

    `pattern` can be either a function or a string.
    """
    if isinstance(pattern, basestring):
        ptn_str = pattern
        pattern = lambda s: fnmatch(s, ptn_str)
    join = os.path.join
    isfile = os.path.isfile
    return [join(path, f) for f in os.listdir(path)
            if isfile(join(path, f)) and pattern(f)]

