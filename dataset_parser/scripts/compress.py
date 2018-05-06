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

from scripts.utils import csv_files_filenames, create_folder
from scripts.calculate_std import calculate_file_stats, calculate_stds_percentages


PYTHON_CODERS = [CoderBasic, CoderPCA, CoderAPCA, CoderCA]


def csv_row_count(input_path, input_filename):
    csv = CSVReader(input_path, input_filename)
    csv.close()
    return csv.total_lines - 4


def code_decode_python(args):
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
    coder_info = c.get_info()
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

    return [coder_info, columns_bits]


def code_decode_cpp(args):
    return [0, 0]


def compress_file(args):
    # read args
    coder, coder_params, decoder = args['coder'], args['coder_params'], args['decoder']
    input_path, input_filename = args['input_path'], args['input_filename']
    output_path = args['output_path']
    compressed_filename = input_filename.replace('.csv', '.c.csv')
    decompressed_filename = input_filename.replace('.csv', '.c.d.csv')

    if coder in PYTHON_CODERS:
        coder_info, columns_bits = code_decode_python(args)
    else:
        coder_info, columns_bits = code_decode_cpp(args)

    # compare
    csv_compare = CSVCompare(input_path, input_filename, output_path, decompressed_filename)
    same_file = csv_compare.compare(coder_params.get('error_threshold'))

    # print results
    logger = args['logger']
    input_file = input_path + "/" + input_filename
    compressed_file = output_path + "/" + compressed_filename
    compressed_size = print_results(coder_info, logger, input_file, compressed_file, same_file)
    return [compressed_size] + columns_bits


def print_results(coder_info, logger, input_file, compressed_file, same_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    logger.info("")
    logger.info("RESULTS")
    if same_file:
        logger.info("--------------------------(same file!)")
    else:
        raise StandardError("ERROR: DIFFERENT FILES!")
    logger.info(coder_info)
    logger.info("ORIGINAL FILE:")
    logger.info("-> name: %s" % input_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(input_size))
    logger.info("COMPRESSED FILE:")
    logger.info("-> name: %s" % compressed_file)
    logger.info("-> size (bytes): %s" % "{:,}".format(compressed_size))
    logger.info("-> %s%% of original" % PrintUtils.percentage(compressed_size, input_size))
    logger.info("")
    return compressed_size

#
# dataset_array = [
#     {'name': 'IRKIS', 'folder': "[1]irkis", 'logger': "irkis.log", 'o_folder': "[1]irkis"},
#     {'name': 'NOAA-SST', 'folder': "[2]noaa-sst/months/2017", 'logger': "noaa-sst.log", 'o_folder': "[2]noaa-sst"},
#     {'name': 'NOAA-ADCP', 'folder': "[3]noaa-adcp/2015", 'logger': "noaa-adcp.log", 'o_folder': "[3]noaa-adcp"},
#     {'name': 'SolarAnywhere', 'folder': "[4]solar-anywhere/2011", 'logger': "solar-anywhere.log", 'o_folder': "[4]solar-anywhere"},
#     {'name': 'ElNino', 'folder': "[5]el-nino", 'logger': "el-nino.log", 'o_folder': "[5]el-nino"},
#     {'name': 'NOAA-SPC-hail', 'folder': "[6]noaa-spc-reports/hail", 'logger': "noaa-spc-hail.log", 'o_folder': "[6]noaa-spc-reports"},
#     {'name': 'NOAA-SPC-tornado', 'folder': "[6]noaa-spc-reports/tornado", 'logger': "noaa-spc-tornado.log", 'o_folder': "[6]noaa-spc-reports"},
#     {'name': 'NOAA-SPC-wind', 'folder': "[6]noaa-spc-reports/wind", 'logger': "noaa-spc-wind.log", 'o_folder': "[6]noaa-spc-reports"}
# ]

dataset_array = [
    # {'name': 'CO2', 'folder': "CO2", 'logger': "CO2.log", 'o_folder': "CO2"},
    # {'name': 'Humidity', 'folder': "Humidity", 'logger': "Humidity.log", 'o_folder': "Humidity"},
    # {'name': 'Lysimeter', 'folder': "Lysimeter", 'logger': "Lysimeter.log", 'o_folder': "Lysimeter"},
    # {'name': 'Moisture', 'folder': "Moisture", 'logger': "Moisture.log", 'o_folder': "Moisture"},
    # {'name': 'Pressure', 'folder': "Pressure", 'logger': "Pressure.log", 'o_folder': "Pressure"},
    # {'name': 'Radiation', 'folder': "Radiation", 'logger': "Radiation.log", 'o_folder': "Radiation"},
    # {'name': 'Snow_height', 'folder': "Snow_height", 'logger': "Snow_height.log", 'o_folder': "Snow_height"},
    # {'name': 'Temperature', 'folder': "Temperature", 'logger': "Temperature.log", 'o_folder': "Temperature"},
    # {'name': 'Voltage', 'folder': "Voltage", 'logger': "Voltage.log", 'o_folder': "Voltage"},
    {'name': 'Wind_direction', 'folder': "Wind_direction", 'logger': "Wind_direction.log", 'o_folder': "Wind_direction"},
    {'name': 'Wind_speed', 'folder': "Wind_speed", 'logger': "Wind_speed.log", 'o_folder': "Wind_speed"},
]

coders_array = [
    {
        'name': 'CoderBasic',
        'coder': CoderBasic,
        'decoder': DecoderBasic,
        'o_folder': 'basic'
    },
    {
        'name': 'CoderPCA',
        'coder': CoderPCA,
        'decoder': DecoderPCA,
        'o_folder': 'pca',
        'params': {'fixed_window_size': [5, 10, 25, 50, 100, 200]}
    },
    {
        'name': 'CoderAPCA',
        'coder': CoderAPCA,
        'decoder': DecoderAPCA,
        'o_folder': 'apca',
        'params': {'max_window_size': [5, 10, 25, 50, 100, 200]}
    },
    {
        'name': 'CoderCA',
        'coder': CoderCA,
        'decoder': DecoderCA,
        'o_folder': 'ca',
        'params': {'max_window_size': [5, 10, 25, 50, 100, 200]}
    },
]


def script(output_filename):
    # datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/"
    datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/results/paper_csv/3-without-outliers/"
    # output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/"
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/paper-output/"

    csv = CSVWriter(output_path, output_filename)
    csv.write_row(['Dataset', 'Filename', '#rows', 'Coder', '%', 'Error Threshold',
                   'Window Param', 'Size (B)', 'CR (%)',
                   'Delta - Size (b)', 'Delta - CR (%)',
                   'Other columns - Size (b)', 'Other columns - CR (%)'])

    for dataset_dictionary in dataset_array:
        run_script_on_dataset(csv, datasets_path, dataset_dictionary, output_path)
    csv.close()


def run_script_on_dataset(csv, datasets_path, dataset_dictionary, output_path):
    input_path = datasets_path + dataset_dictionary['folder']
    logger_name = dataset_dictionary['logger']
    logger = setup_logger(logger_name, logger_name)

    output_dataset_path = output_path + dataset_dictionary['o_folder']
    create_folder(output_dataset_path)

    for id1, input_filename in enumerate(csv_files_filenames(input_path)):
        row = [dataset_dictionary['name']] if id1 == 0 else [None]
        run_script_on_file(csv, id1, row, logger, input_path, input_filename, output_dataset_path)


def run_script_on_file(csv, id1, row, logger, input_path, input_filename, output_dataset_path):
    base_values = None
    row_count = PrintUtils.separate(csv_row_count(input_path, input_filename))

    # calculate error thresholds
    percentages = [0, 3, 5, 10, 15, 20, 30]
    stds = calculate_file_stats(input_path, input_filename)
    thresholds_hash = calculate_stds_percentages(stds, percentages)

    for id2, coder_dictionary in enumerate(coders_array):
        if id1 == 0 and id2 == 0:  # first row of dataset and file
            row += [input_filename, row_count]
        elif id2 == 0:  # first row of file
            row = [None, input_filename, row_count]
        else:
            row = [None, None, None]
        base_values = run_script_on_coder(csv, row, coder_dictionary, output_dataset_path, logger,
                                          input_path, input_filename, base_values, thresholds_hash)


def run_script_on_coder(csv, row, coder_dictionary, output_dataset_path, logger, input_path, input_filename, base_values, thresholds_hash):
    output_dataset_coder_path = output_dataset_path + '/' + coder_dictionary['o_folder']
    create_folder(output_dataset_coder_path)

    # CoderBasic - no params
    if coder_dictionary['name'] == 'CoderBasic':
        values = [coder_dictionary['name']] + [None] * 3
        args = {
            'logger': logger,
            'coder': coder_dictionary['coder'],
            'coder_params': {},
            'decoder': coder_dictionary['decoder'],
            'input_path': input_path,
            'input_filename': input_filename,
            'output_path': output_dataset_coder_path
        }
        compression_values = compress_file(args)
        base_values = out_results(base_values, compression_values, row + values, csv)
    else:
        # CoderPCA, CoderAPCA and CoderCA
        window_param_name = coder_dictionary['params'].keys()[0]  # there's a single key
        window_sizes = coder_dictionary['params'][window_param_name]
        percentages = thresholds_hash.keys()

        for id3, percentage in enumerate(percentages):
            error_thresold_array = thresholds_hash[percentage]
            params = {'error_threshold': error_thresold_array}
            for id4, window_size in enumerate(window_sizes):
                values = [coder_dictionary['name']] if id3 == 0 and id4 == 0 else [None]
                values += [percentage, params['error_threshold']] if id4 == 0 else [None, None]
                values += [window_size]

                params[window_param_name] = window_size
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
                base_values = out_results(base_values, compression_values, row + values, csv)
    return base_values


def out_results(base_values, compression_values, row, csv):
    values = []
    if base_values is None:
        base_values = compression_values
        for value in compression_values:
            values += [PrintUtils.separate(value), 100]
    else:
        for idx, value in enumerate(compression_values):
            percentage = PrintUtils.percentage(value, base_values[idx])
            values += [PrintUtils.separate(value), PrintUtils.separate(percentage)]
    csv.write_row(row + values)
    return base_values

script("results.csv")
