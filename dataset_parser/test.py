from bit_stream.utils import Utils
from coders.utils import Utils as CodersUtils
from scripts.scripts import clean_file

# original file
input_path, input_filename = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis", "vwc_1202.dat"

parser_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser"

# one value per line file
clean_filename = input_filename + '.clean'
# clean_file(input_path, input_filename, parser_path, clean_filename)

# BASE
# CodersUtils.code_decode('base', parser_path, clean_filename, parser_path)
# Utils.compare_files(parser_path, clean_filename, clean_filename + '.base.code.decode')

# PCA
CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path)

# APCA
# CodersUtils.code_decode('apca', parser_path, clean_filename, parser_path)

# compare size

# compare with one value per line file