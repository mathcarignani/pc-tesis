from bit_stream.utils import Utils as BitStreamUtils
from coders.utils import Utils as CodersUtils
from file_utils.scripts import Scripts as FileScripts
from scripts.scripts import clean_file

# original file
input_path, input_filename = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis", "vwc_1202.dat"

parser_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser"

# one value per line file
clean_filename = input_filename + '.clean'
# clean_file(input_path, input_filename, parser_path, clean_filename)

# # BASE
CodersUtils.code_decode('base', parser_path, clean_filename, parser_path)

# PCA
coder_params = {'error_threshold': 5, 'fixed_window_size': 10}
CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)
coder_params = {'error_threshold': 10, 'fixed_window_size': 10}
CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)
coder_params = {'error_threshold': 1000, 'fixed_window_size': 10}
CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)
coder_params = {'error_threshold': 1000, 'fixed_window_size': 11}
CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)
coder_params = {'error_threshold': 1000, 'fixed_window_size': 15}
CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)

# APCA
# coder_params = {'error_threshold': 5, 'fixed_window_size': 10}
# CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)
# coder_params = {'error_threshold': 10, 'fixed_window_size': 10}
# CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)
# coder_params = {'error_threshold': 1000, 'fixed_window_size': 10}
# CodersUtils.code_decode('pca', parser_path, clean_filename, parser_path, coder_params)


# compare size

# compare with one value per line file