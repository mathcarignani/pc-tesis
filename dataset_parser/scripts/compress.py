import sys
sys.path.append('.')

import os

from aux.logger import setup_logger
from aux.print_utils import PrintUtils
from file_utils.csv_utils.csv_compare import CSVCompare
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

from coders.basic.coder_basic import CoderBasic
from coders.basic.decoder_basic import DecoderBasic
from coders.pca.coder_pca import CoderPCA
from coders.pca.decoder_pca import DecoderPCA


def compress(args):
    # read args
    coder, coder_params, decoder = args['coder'], args['coder_params'], args['decoder']
    input_path, input_filename = args['input_path'], args['input_filename']
    output_path = args['output_path']
    compressed_filename, decompressed_filename = args['compressed_filename'], args['decompressed_filename']

    # code
    input_csv = CSVReader(input_path, input_filename, True)
    c = coder(input_csv, output_path, compressed_filename, coder_params)
    c.code_file()
    c.close()

    # decode
    output_csv = CSVWriter(output_path, decompressed_filename)
    d = decoder(output_path, compressed_filename, output_csv, coder_params)
    try:
        d.decode_file()
    except AssertionError as e:
        if e == "Reached EOF.":
            print "ERROR: Reached End Of File."
    d.close()

    # compare
    compare = CSVCompare(input_path, input_filename, output_path, decompressed_filename)
    same_file = compare.compare(coder_params.get('error_threshold') or 0)

    # print results
    logger = args['logger']
    input_file = input_path + "/" + input_filename
    compressed_file = output_path + "/" + compressed_filename
    print_results(c, logger, input_file, compressed_file, same_file)


def print_results(c, logger, input_file, compressed_file, same_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    logger.info
    logger.info("RESULTS")
    if same_file:
        logger.info("--------------------------(same file!)")
    else:
        logger.info("--------------------------(failure)")
    logger.info(c.get_info())
    logger.info("ORIGINAL FILE:")
    logger.info("-> name: %s" % input_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(input_size))
    logger.info("COMPRESSED FILE:")
    logger.info("-> name: %s" % compressed_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(compressed_size))
    logger.info("-> %s%% of original" % PrintUtils.percentage(compressed_size, input_size))
    logger.info


def compress_file(logger, input_path, input_filename, coder, decoder, coder_params={}):
    args = {
        'logger': logger,
        'coder': coder,
        'coder_params': coder_params,
        'decoder': decoder,
        'input_path': input_path,
        'input_filename': input_filename,
        'output_path': '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output',
        'compressed_filename': input_filename.replace('.csv', '.c.csv'),
        'decompressed_filename': input_filename.replace('.csv', '.c.d.csv')
    }
    compress(args)


def compress_path(logger, input_path, coder, decoder, coder_params={}):
    input_filenames = os.listdir(input_path)
    input_filenames = [f for f in input_filenames if os.path.isfile(os.path.join(input_path, f))]
    input_filenames = [f for f in input_filenames if f.endswith(".csv")]
    for input_filename in input_filenames:
        compress_file(logger, input_path, input_filename, coder, decoder, coder_params)
#
# input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[1]irkis"
# logger = setup_logger('irkis.log', 'irkis.log')
# compress_path(logger, input_path, CoderBasic, DecoderBasic)
#
# input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[2]noaa-sst/months/2017"
# logger = setup_logger('noaa-sst.log', 'noaa-sst.log')
# compress_path(logger, input_path, CoderBasic, DecoderBasic)
#
# input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[3]noaa-adcp/2012"
# logger = setup_logger('noaa-adcp.log', 'noaa-adcp.log')
# compress_path(logger, input_path, CoderBasic, DecoderBasic)
#
# input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[4]solar-anywhere/2011"
# logger = setup_logger('solar-anywhere.log', 'solar-anywhere.log')
# compress_path(logger, input_path, CoderBasic, DecoderBasic)
#
# input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[5]el-nino"
# logger = setup_logger('el-nino.log', 'el-nino.log')
# compress_path(logger, input_path, CoderBasic, DecoderBasic)

input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[5]el-nino"
logger = setup_logger('el-nino.log', 'el-nino.log')
compress_path(logger, input_path, CoderPCA, DecoderPCA, {'error_threshold': 0, 'fixed_window_size': 5})




# folders = ['[1]irkis', ['[2]n']]


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
