import os


def full_path(path, filename):
    return path + "/" + filename


# Return file size in bytes.
def file_size(path, filename):
    full_p = full_path(path, filename)
    statinfo = os.stat(full_p)
    return statinfo.st_size
