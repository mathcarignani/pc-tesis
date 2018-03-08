import sys
sys.path.append('.')

import os

from aux.print_utils import PrintUtils
from file_utils.csv_utils.csv_compare import CSVCompare
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

from coders.coder_base import CoderBase
from coders.decoder_base import DecoderBase
from coders.pca.coder_pca import CoderPCA
from coders.pca.decoder_pca import DecoderPCA

from parsers.adcp.parser_adcp import ParserADCP
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA
from parsers.solar_anywhere.parser_solar_anywhere import ParserSolarAnywhere


def compress(args):
    # read args
    parser, coder, decoder = args['parser'], args['coder'], args['decoder']
    input_path, input_filename = args['input_path'], args['input_filename']
    output_path = args['output_path']
    compressed_filename, decompressed_filename = args['compressed_filename'], args['decompressed_filename']

    # code
    input_csv = CSVReader(input_path, input_filename, True)
    row1, row2 = input_csv.read_line(), input_csv.read_line()
    c = coder(parser, input_csv, output_path, compressed_filename)
    c.code_file()
    c.close()

    # # decode
    # output_csv = CSVWriter(output_path, decompressed_filename)
    # output_csv.write_row(row1), output_csv.write_row(row2)
    # d = decoder(parser, output_path, compressed_filename, output_csv, len(row2)-1)
    # d.decode_file()
    # d.close()
    #
    # # compare
    # compare = CSVCompare(input_path, input_filename, output_path, decompressed_filename)
    # compare.compare()
    #
    # print results
    print_results(input_path + "/" + input_filename, output_path + "/" + compressed_filename)


def print_results(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    print
    print "RESULTS"
    print "--------------------------"
    print "ORIGINAL FILE:"
    print "-> name: %s" % input_file
    print "-> size (bytes): %s" % "{:,}".format(input_size)
    print "COMPRESSED FILE:"
    print "-> name: %s" % compressed_file
    print "-> size (bytes): %s" % "{:,}".format(compressed_size)
    print "-> %s%% of original" % PrintUtils.percentage(compressed_size, input_size)
    print


def compress_noaa(coder, decoder):
    args = {
        'parser': ParserNOAA,
        'coder': coder,
        'decoder': decoder,
        'input_path': '/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[2]noaa-buoy/months/2017',
        'input_filename': 'noaa-buoy-201712.csv',
        'output_path': '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output',
        'compressed_filename': 'noaa-buoy-201712.c.csv',
        'decompressed_filename': 'noaa-buoy-201712.c.d.csv'
    }
    compress(args)

# compress_noaa(CoderBase, DecoderBase)
compress_noaa(CoderPCA, DecoderPCA)
