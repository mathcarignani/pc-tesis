from bit_stream.utils import Utils as BitStreamUtils
from coders.utils import Utils as CodersUtils

input_path, input_filename = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis", "vwc_1202.dat"
parser_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser"

CodersUtils.code_decode('base', input_path, input_filename, parser_path)
CodersUtils.code_decode('pca', input_path, input_filename, parser_path)
CodersUtils.code_decode('apca', input_path, input_filename, parser_path)

print "Comparing"
BitStreamUtils.compare_files(parser_path, "vwc_1202.dat.base.code.decode", "vwc_1202.dat.pca.code.decode")
BitStreamUtils.compare_files(parser_path, "vwc_1202.dat.base.code.decode", "vwc_1202.dat.apca.code.decode")
