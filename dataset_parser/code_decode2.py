from coders.coder_base import CoderBase
from coders.decoder_base import DecoderBase

input_path, input_filename = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis", "vwc_1202.dat"
output_path, output_filename = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser", "vwc_1202.dat.code"

cb = CoderBase(input_path, input_filename, output_path, output_filename)
cb.code()
cb.close()

decode_path, decode_filename = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser", "vwc_1202.dat.code.decode"
db = DecoderBase(output_path, output_filename, decode_path, decode_filename)
db.decode()
db.close()
