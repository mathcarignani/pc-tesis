import sys
sys.path.append('.')


class GZipCommon(object):
    OUT_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/gzip_compare/out"
    FILENAME = {False: 'results.csv', True: 'results-t.csv'}  # use FILENAME[transpose]
