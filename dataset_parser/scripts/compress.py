import sys
sys.path.append('.')

import os

from aux.logger import setup_logger
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
    parser, coder, coder_params, decoder = args['parser'], args['coder'], args['coder_params'], args['decoder']
    input_path, input_filename = args['input_path'], args['input_filename']
    output_path = args['output_path']
    compressed_filename, decompressed_filename = args['compressed_filename'], args['decompressed_filename']

    # code
    input_csv = CSVReader(input_path, input_filename, True)
    c = coder(parser, input_csv, output_path, compressed_filename, coder_params)
    c.code_file()
    c.close()

    # decode
    output_csv = CSVWriter(output_path, decompressed_filename)
    d = decoder(parser, output_path, compressed_filename, output_csv, coder_params)
    try:
        d.decode_file()
    except AssertionError as e:
        if e == "Reached EOF.":
            print "ERROR: Reached End Of File."
    d.close()

    # compare
    compare = CSVCompare(input_path, input_filename, output_path, decompressed_filename)
    compare.compare(coder_params.get('error_threshold') or 0)

    # print results
    logger = args['logger']
    print_results(c, logger, input_path + "/" + input_filename, output_path + "/" + compressed_filename)


def print_results(c, logger, input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    logger.info
    logger.info("RESULTS")
    logger.info("--------------------------")
    logger.info(c.get_info())
    logger.info("ORIGINAL FILE:")
    logger.info("-> name: %s" % input_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(input_size))
    logger.info("COMPRESSED FILE:")
    logger.info("-> name: %s" % compressed_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(compressed_size))
    logger.info("-> %s%% of original" % PrintUtils.percentage(compressed_size, input_size))
    logger.info


def compress_noaa(logger, coder, decoder, coder_params={}):
    args = {
        'logger': logger,
        'parser': ParserNOAA,
        'coder': coder,
        'coder_params': coder_params,
        'decoder': decoder,
        'input_path': '/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[2]noaa-sst/months/2017',
        'input_filename': 'noaa-buoy-201712.csv',
        'output_path': '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output',
        'compressed_filename': 'noaa-buoy-201712.c.csv',
        'decompressed_filename': 'noaa-buoy-201712.c.d.csv'
    }
    compress(args)

logger = setup_logger('log.log', 'log.log')
compress_noaa(logger, CoderBase, DecoderBase)

# logger = setup_logger('log.log', 'log.log')
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 100, 'fixed_window_size': 5})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 100, 'fixed_window_size': 10})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 100, 'fixed_window_size': 20})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 50, 'fixed_window_size': 5})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 50, 'fixed_window_size': 10})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 50, 'fixed_window_size': 20})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 10, 'fixed_window_size': 5})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 10, 'fixed_window_size': 10})
# compress_noaa(logger, CoderPCA, DecoderPCA, {'error_threshold': 10, 'fixed_window_size': 20})
