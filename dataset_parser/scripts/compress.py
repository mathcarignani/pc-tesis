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
from coders.apca.coder_apca import CoderAPCA
from coders.apca.decoder_apca import DecoderAPCA
from coders.ca.coder_ca import CoderCA
from coders.ca.decoder_ca import DecoderCA



def csv_files_filenames(input_path):
    input_filenames = os.listdir(input_path)
    input_filenames = [f for f in input_filenames if os.path.isfile(os.path.join(input_path, f))]
    input_filenames = [f for f in input_filenames if f.endswith(".csv")]
    return input_filenames


def csv_row_count(input_path, input_filename):
    csv = CSVReader(input_path, input_filename)
    csv.close()
    return csv.total_lines - 4


def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def compress_file(args):
    # read args
    coder, coder_params, decoder = args['coder'], args['coder_params'], args['decoder']
    input_path, input_filename = args['input_path'], args['input_filename']
    output_path = args['output_path']
    compressed_filename = input_filename.replace('.csv', '.c.csv')
    decompressed_filename = input_filename.replace('.csv', '.c.d.csv')

    # code
    input_csv = CSVReader(input_path, input_filename, True)
    c = coder(input_csv, output_path, compressed_filename, coder_params)
    c.code_file()
    c.close()
    columns_bits = [column_code.total_bits for column_code in c.dataset.column_code_array]

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
    csv_compare = CSVCompare(input_path, input_filename, output_path, decompressed_filename)
    same_file = csv_compare.compare(coder_params.get('error_threshold') or 0)

    # print results
    logger = args['logger']
    input_file = input_path + "/" + input_filename
    compressed_file = output_path + "/" + compressed_filename
    compressed_size = print_results(c, logger, input_file, compressed_file, same_file)
    return [compressed_size] + columns_bits


def print_results(c, logger, input_file, compressed_file, same_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    logger.info("")
    logger.info("RESULTS")
    if same_file:
        logger.info("--------------------------(same file!)")
    else:
        raise StandardError("ERROR: DIFFERENT FILES!")
    logger.info(c.get_info())
    logger.info("ORIGINAL FILE:")
    logger.info("-> name: %s" % input_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(input_size))
    logger.info("COMPRESSED FILE:")
    logger.info("-> name: %s" % compressed_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(compressed_size))
    logger.info("-> %s%% of original" % PrintUtils.percentage(compressed_size, input_size))
    logger.info("")
    return compressed_size


dataset_array = [
    # {'name': 'IRKIS', 'folder': "[1]irkis", 'logger': "irkis.log", 'o_folder': "[1]irkis"},
    # {'name': 'NOAA-SST', 'folder': "[2]noaa-sst/months/2017", 'logger': "noaa-sst.log", 'o_folder': "[2]noaa-sst"},
    {'name': 'NOAA-ADCP', 'folder': "[3]noaa-adcp/2015", 'logger': "noaa-adcp.log", 'o_folder': "[3]noaa-adcp"},
    {'name': 'SolarAnywhere', 'folder': "[4]solar-anywhere/2011", 'logger': "solar-anywhere.log", 'o_folder': "[4]solar-anywhere"},
    {'name': 'ElNino', 'folder': "[5]el-nino", 'logger': "el-nino.log", 'o_folder': "[5]el-nino"}
]

coders_array = [
    {
        'name': 'CoderBasic',
        'coder': CoderBasic,
        'decoder': DecoderBasic,
        'o_folder': 'basic',
        'params': [{}]
    },
    # {
    #     'name': 'CoderPCA',
    #     'coder': CoderPCA,
    #     'decoder': DecoderPCA,
    #     'o_folder': 'pca',
    #     'params': [
    #         {'error_threshold': 0, 'fixed_window_size': 5},
    #         # {'error_threshold': 0, 'fixed_window_size': 10},
    #         # {'error_threshold': 0, 'fixed_window_size': 20},
    #         # {'error_threshold': 0, 'fixed_window_size': 40},
    #         {'error_threshold': 0, 'fixed_window_size': 100},
    #         {'error_threshold': 10, 'fixed_window_size': 5},
    #         {'error_threshold': 10, 'fixed_window_size': 10},
    #         {'error_threshold': 10, 'fixed_window_size': 20},
    #         {'error_threshold': 10, 'fixed_window_size': 40},
    #         {'error_threshold': 10, 'fixed_window_size': 100},
    #         {'error_threshold': 25, 'fixed_window_size': 5},
    #         {'error_threshold': 25, 'fixed_window_size': 10},
    #         {'error_threshold': 25, 'fixed_window_size': 20},
    #         {'error_threshold': 25, 'fixed_window_size': 40},
    #         {'error_threshold': 25, 'fixed_window_size': 100},
    #         # {'error_threshold': 50, 'fixed_window_size': 5},
    #         # {'error_threshold': 50, 'fixed_window_size': 10},
    #         # {'error_threshold': 50, 'fixed_window_size': 20},
    #         # {'error_threshold': 50, 'fixed_window_size': 40},
    #         {'error_threshold': 50, 'fixed_window_size': 100},
    #         # {'error_threshold': 100, 'fixed_window_size': 5},
    #         # {'error_threshold': 100, 'fixed_window_size': 10},
    #         # {'error_threshold': 100, 'fixed_window_size': 20},
    #         # {'error_threshold': 100, 'fixed_window_size': 40},
    #         {'error_threshold': 100, 'fixed_window_size': 100},
    #         # {'error_threshold': 250, 'fixed_window_size': 5},
    #         # {'error_threshold': 250, 'fixed_window_size': 10},
    #         # {'error_threshold': 250, 'fixed_window_size': 20},
    #         # {'error_threshold': 250, 'fixed_window_size': 40},
    #         {'error_threshold': 250, 'fixed_window_size': 100},
    #         # {'error_threshold': 500, 'fixed_window_size': 5},
    #         # {'error_threshold': 500, 'fixed_window_size': 10},
    #         # {'error_threshold': 500, 'fixed_window_size': 20},
    #         # {'error_threshold': 500, 'fixed_window_size': 40},
    #         {'error_threshold': 500, 'fixed_window_size': 100}
    #     ]
    # },
    # {
    #     'name': 'CoderAPCA',
    #     'coder': CoderAPCA,
    #     'decoder': DecoderAPCA,
    #     'o_folder': 'apca',
    #     'params': [
    #         # {'error_threshold': 0, 'max_window_size': 5},
    #         # {'error_threshold': 0, 'max_window_size': 10},
    #         # {'error_threshold': 0, 'max_window_size': 20},
    #         # {'error_threshold': 0, 'max_window_size': 40},
    #         {'error_threshold': 0, 'max_window_size': 100},
    #         {'error_threshold': 10, 'max_window_size': 5},
    #         {'error_threshold': 10, 'max_window_size': 10},
    #         {'error_threshold': 10, 'max_window_size': 20},
    #         {'error_threshold': 10, 'max_window_size': 40},
    #         {'error_threshold': 10, 'max_window_size': 100},
    #         {'error_threshold': 25, 'max_window_size': 5},
    #         {'error_threshold': 25, 'max_window_size': 10},
    #         {'error_threshold': 25, 'max_window_size': 20},
    #         {'error_threshold': 25, 'max_window_size': 40},
    #         {'error_threshold': 25, 'max_window_size': 100},
    #         # {'error_threshold': 50, 'max_window_size': 5},
    #         # {'error_threshold': 50, 'max_window_size': 10},
    #         # {'error_threshold': 50, 'max_window_size': 20},
    #         # {'error_threshold': 50, 'max_window_size': 40},
    #         {'error_threshold': 50, 'max_window_size': 100},
    #         # {'error_threshold': 100, 'max_window_size': 5},
    #         # {'error_threshold': 100, 'max_window_size': 10},
    #         # {'error_threshold': 100, 'max_window_size': 20},
    #         # {'error_threshold': 100, 'max_window_size': 40},
    #         {'error_threshold': 100, 'max_window_size': 100},
    #         # {'error_threshold': 250, 'max_window_size': 5},
    #         # {'error_threshold': 250, 'max_window_size': 10},
    #         # {'error_threshold': 250, 'max_window_size': 20},
    #         # {'error_threshold': 250, 'max_window_size': 40},
    #         {'error_threshold': 250, 'max_window_size': 100},
    #         # {'error_threshold': 500, 'max_window_size': 5},
    #         # {'error_threshold': 500, 'max_window_size': 10},
    #         # {'error_threshold': 500, 'max_window_size': 20},
    #         # {'error_threshold': 500, 'max_window_size': 40},
    #         {'error_threshold': 500, 'max_window_size': 100},
    #     ]
    # },
    {
        'name': 'CoderCA',
        'coder': CoderCA,
        'decoder': DecoderCA,
        'o_folder': 'ca',
        'params': [
            {'error_threshold': 0, 'max_window_size': 5},
            {'error_threshold': 0, 'max_window_size': 10},
            {'error_threshold': 0, 'max_window_size': 20},
            {'error_threshold': 0, 'max_window_size': 40},
            {'error_threshold': 0, 'max_window_size': 100},
            {'error_threshold': 10, 'max_window_size': 5},
            {'error_threshold': 10, 'max_window_size': 10},
            {'error_threshold': 10, 'max_window_size': 20},
            {'error_threshold': 10, 'max_window_size': 40},
            {'error_threshold': 10, 'max_window_size': 100},
            {'error_threshold': 25, 'max_window_size': 5},
            {'error_threshold': 25, 'max_window_size': 10},
            {'error_threshold': 25, 'max_window_size': 20},
            {'error_threshold': 25, 'max_window_size': 40},
            {'error_threshold': 25, 'max_window_size': 100},
            {'error_threshold': 50, 'max_window_size': 5},
            {'error_threshold': 50, 'max_window_size': 10},
            {'error_threshold': 50, 'max_window_size': 20},
            {'error_threshold': 50, 'max_window_size': 40},
            {'error_threshold': 50, 'max_window_size': 100},
            {'error_threshold': 100, 'max_window_size': 5},
            {'error_threshold': 100, 'max_window_size': 10},
            {'error_threshold': 100, 'max_window_size': 20},
            {'error_threshold': 100, 'max_window_size': 40},
            {'error_threshold': 100, 'max_window_size': 100},
            {'error_threshold': 250, 'max_window_size': 5},
            {'error_threshold': 250, 'max_window_size': 10},
            {'error_threshold': 250, 'max_window_size': 20},
            {'error_threshold': 250, 'max_window_size': 40},
            {'error_threshold': 250, 'max_window_size': 100},
            {'error_threshold': 500, 'max_window_size': 5},
            {'error_threshold': 500, 'max_window_size': 10},
            {'error_threshold': 500, 'max_window_size': 20},
            {'error_threshold': 500, 'max_window_size': 40},
            {'error_threshold': 500, 'max_window_size': 100},
        ]
    },
]


def script():
    datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/"
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/"
    csv = CSVWriter(output_path, 'results.csv')
    csv.write_row(['Dataset', 'Filename', '#rows', 'Coder', 'Params', 'Size (B)', 'Compression Rate (%)'])
    for dataset_dictionary in dataset_array:
        row = [dataset_dictionary['name']]

        input_path = datasets_path + dataset_dictionary['folder']
        logger_name = dataset_dictionary['logger']
        logger = setup_logger(logger_name, logger_name)

        output_dataset_path = output_path + dataset_dictionary['o_folder']
        create_folder(output_dataset_path)

        for id1, input_filename in enumerate(csv_files_filenames(input_path)):
            values = [input_filename, PrintUtils.separate(csv_row_count(input_path, input_filename))]
            row = row + values if id1 == 0 else [None] + values
            base_values = None

            for id2, coder_dictionary in enumerate(coders_array):
                values = [coder_dictionary['name']]
                row = row + values if id2 == 0 else [None, None, None] + values

                output_dataset_coder_path = output_dataset_path + '/' + coder_dictionary['o_folder']
                create_folder(output_dataset_coder_path)

                for id3, params in enumerate(coder_dictionary['params']):
                    values = [params]
                    row = row + values if id3 == 0 else [None, None, None, None] + values
                    args = {
                        'logger': logger,
                        'coder': coder_dictionary['coder'],
                        'coder_params': params,
                        'decoder': coder_dictionary['decoder'],
                        'input_path': input_path,
                        'input_filename': input_filename,
                        'output_path': output_dataset_coder_path
                    }
                    compression_values = compress_file(args)
                    if base_values is None:
                        base_values = compression_values
                        for value in compression_values:
                            row += [PrintUtils.separate(value), 100]
                    else:
                        for idx, value in enumerate(compression_values):
                            percentage = PrintUtils.percentage(value, base_values[idx])
                            row += [PrintUtils.separate(value), PrintUtils.separate(percentage)]
                    csv.write_row(row)
    csv.close()

script()
