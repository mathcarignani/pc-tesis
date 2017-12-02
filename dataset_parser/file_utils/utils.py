import os


class Utils(object):
    @staticmethod
    def full_path(path, filename):
        return path + "/" + filename

    # Return file size in bytes.
    @staticmethod
    def file_size(path, filename):
        full_path = Utils.full_path(path, filename)
        statinfo = os.stat(full_path)
        return statinfo.st_size
