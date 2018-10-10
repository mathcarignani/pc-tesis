import sys
sys.path.append('.')

import os

from auxi.logger import setup_logger
from auxi.print_utils import PrintUtils
from auxi.os_utils import git_path
from file_utils.csv_utils.csv_compare import CSVCompare
from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.csv_utils.csv_utils import CSVUtils
from file_utils.bit_stream.utils import BitStreamUtils
from scripts.utils import csv_files_filenames, create_folder
from scripts.compress.calculate_std import calculate_file_stats, calculate_stds_percentages
from scripts.compress.compress_aux import THRESHOLD_PERCENTAGES, CSV_PATH, DATASETS_ARRAY, CODERS_ARRAY
from scripts.compress.compress_cpp import code_decode_cpp
from scripts.compress.compress_args import CompressArgs


def compress_decompress_compare(args):
    print "Compressing and decompressing files..."
    coder_info, columns_bits, column_mask_bits = code_decode_cpp(args)
    print "Comparing original and decompressed files..."
    csv_compare = CSVCompare(args.input_path, args.input_filename, args.output_path, args.deco_filename)
    same_file = csv_compare.compare(args.coder_params.get('error_threshold'), False)
    if not same_file:
        print "ERROR / ERROR / ERROR"
    # assert same_file

    return [coder_info, columns_bits, column_mask_bits, same_file]


def compress_file(args):
    coder_info, columns_bits, column_mask_bits, same_file = compress_decompress_compare(args)

    # print results
    input_file = args.input_path + "/" + args.input_filename
    compressed_file = args.output_path + "/" + args.compressed_filename
    compressed_size = print_results(coder_info, args.logger, input_file, compressed_file, same_file)
    size_check(compressed_size, columns_bits, column_mask_bits)
    compression_values = []
    for i in range(0, len(columns_bits)):
        compression_values.append(columns_bits[i])
        compression_values.append(column_mask_bits[i])
        compression_values.append(columns_bits[i] + column_mask_bits[i])
    return [compressed_size] + compression_values


def size_check(compressed_size, columns_bits, column_mask_bits):
    columns_bytes = sum(columns_bits + column_mask_bits)/8
    diff = compressed_size - columns_bytes
    max_header_size = 15000
    if diff >= max_header_size:
        print 'DIFF = %s' % diff
    assert(diff < max_header_size)


def print_results(coder_info, logger, input_file, compressed_file, same_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    logger.info("")
    logger.info("RESULTS")
    if same_file:
        logger.info("--------------------------(same file!)")
    else:
        logger.info("ERROR: DIFFERENT FILES!")
        # raise StandardError("ERROR: DIFFERENT FILES!")
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


def script(output_filename):
    datasets_path = CSV_PATH
    # datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/results/paper_csv/3-without-outliers/"
    output_path = git_path() + "/dataset_parser/scripts/compress/output/"
    # output_path = python_git_path() + "/dataset_parser/scripts/paper-output/"

    csv = CSVWriter(output_path, output_filename)
    row = ['Dataset', 'Filename', '#rows', 'Coder', '%', 'Error Threshold', 'Window Param', 'Size (B)', 'CR (%)',
           'Delta - Size (data)', 'Delta - Size (mask)', 'Delta - Size (total)', 'Delta - CR (%)',
           'Other columns - Size (data)', 'Other columns - Size (mask)', 'Other columns - Size (total)', 'Other columns - CR (%)']
    csv.write_row(row)

    for dataset_dictionary in DATASETS_ARRAY:
        run_script_on_dataset(csv, datasets_path, dataset_dictionary, output_path)
    csv.close()


def run_script_on_dataset(csv, datasets_path, dataset_dictionary, output_path):
    input_path = datasets_path + dataset_dictionary['folder']
    logger_name = dataset_dictionary['logger']
    logger = setup_logger(logger_name, logger_name)

    output_dataset_path = output_path + dataset_dictionary['o_folder']
    create_folder(output_dataset_path)
    name = dataset_dictionary['name']

    for id1, input_filename in enumerate(csv_files_filenames(input_path)):
        if name in ["NOAA-SST", "NOAA-ADCP"] and id1 >= 2:
            return
        row = [dataset_dictionary['name']] if id1 == 0 else [None]
        run_script_on_file(csv, id1, row, logger, input_path, input_filename, output_dataset_path)


def run_script_on_file(csv, id1, row, logger, input_path, input_filename, output_dataset_path):
    base_values = None
    row_count = PrintUtils.separate(CSVUtils.csv_row_count(input_path, input_filename))

    # calculate error thresholds
    stds = calculate_file_stats(input_path, input_filename)
    thresholds_hash = calculate_stds_percentages(stds, THRESHOLD_PERCENTAGES)

    for id2, coder_dictionary in enumerate(CODERS_ARRAY):
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

    coder_name = coder_dictionary['name']
    # CoderBasic - no params
    if coder_name == 'CoderBasic':
        values = [coder_name] + [None] * 3
        args = {
            'logger': logger,
            'coder': coder_dictionary.get('coder'),
            'coder_name': coder_dictionary['name'],
            'coder_params': {},
            'decoder': coder_dictionary.get('decoder'),
            'input_path': input_path,
            'input_filename': input_filename,
            'output_path': output_dataset_coder_path
        }
        compress_args = CompressArgs(args)
        compression_values = compress_file(compress_args)
        base_values = out_results(base_values, compression_values, row + values, csv)
    else:
        # other coders
        window_param_name = coder_dictionary['params'].keys()[0]  # there's a single key
        window_sizes = coder_dictionary['params'][window_param_name]
        percentages = thresholds_hash.keys()

        for id3, percentage in enumerate(percentages):
            error_thresold_array = thresholds_hash[percentage]
            params = {'error_threshold': error_thresold_array}
            for id4, window_size in enumerate(window_sizes):
                values = [coder_name] if id3 == 0 and id4 == 0 else [None]
                values += [percentage, params['error_threshold']] if id4 == 0 else [None, None]
                values += [window_size]

                params[window_param_name] = window_size
                args = {
                    'logger': logger,
                    'coder': coder_dictionary.get('coder'),
                    'coder_name': coder_dictionary['name'],
                    'coder_params': params,
                    'decoder': coder_dictionary.get('decoder'),
                    'input_path': input_path,
                    'input_filename': input_filename,
                    'output_path': output_dataset_coder_path
                }
                compress_args = CompressArgs(args)
                compression_values = compress_file(compress_args)
                base_values = out_results(base_values, compression_values, row + values, csv)
    return base_values


def out_results(base_values, compression_values, row, csv):
    values = []
    if base_values is None:
        base_values = compression_values
        for idx, value in enumerate(compression_values):
            if (idx % 3) == 0:  # idx is 0, 3, 6, 9, 12, etc.
                val = PrintUtils.separate(value) if idx == 0 else value
                values += [val, 100]
            else:
                values += [value]
    else:
        for idx, value in enumerate(compression_values):
            if (idx % 3) == 0:  # idx is 0, 3, 6, 9, 12, etc.
                percentage = PrintUtils.percentage(value, base_values[idx])
                val = PrintUtils.separate(value) if idx == 0 else value
                values += [val, PrintUtils.separate(percentage)]
            else:
                values += [value]
    csv.write_row(row + values)
    return base_values


def compare():
    path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/[6]noaa-spc-reports/basic"
    file1 = "noaa_spc-wind.c.cpp.csv"
    file2 = "noaa_spc-wind.c.python.csv"
    path1 = path + "/" + file1
    path2 = path + "/" + file2
    print file1 + " " + str(os.path.getsize(path1))
    print file2 + " " + str(os.path.getsize(path2))
    assert(BitStreamUtils.compare_files(path, file1, path, file2))

script("results.csv")
# compare()
