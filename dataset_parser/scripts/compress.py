import sys
sys.path.append('.')

import os
import time

from aux.logger import setup_logger
from aux.print_utils import PrintUtils
from file_utils.csv_utils.csv_compare import CSVCompare
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.csv_utils.csv_utils import CSVUtils
from file_utils.bit_stream.utils import BitStreamUtils
from scripts.utils import csv_files_filenames, create_folder
from scripts.calculate_std import calculate_file_stats, calculate_stds_percentages
from scripts.compress_aux import PYTHON_CODERS, dataset_array, coders_array
from scripts.compress_cpp import code_cpp, decode_cpp, code_decode_cpp
from scripts.compress_args import CompressArgs


def code_python(args):
    start_time = time.time()
    args.code_python()
    input_csv = CSVReader(args.input_path, args.input_filename, True)
    c = args.coder(input_csv, args.output_path, args.compressed_filename, args.coder_params)
    c.code_file()
    c.close()
    coder_info = c.get_info()
    columns_bits = [column_code.total_bits for column_code in c.dataset.column_code_array]
    elapsed_time = time.time() - start_time
    print args.input_filename, "code_python - elapsed time =", round(elapsed_time, 2), "seconds"
    return [coder_info, columns_bits]


def decode_python(args):
    start_time = time.time()
    args.decode_python()
    output_csv = CSVWriter(args.output_path, args.deco_filename)
    d = args.decoder(args.output_path, args.compressed_filename, output_csv, args.coder_params)
    try:
        d.decode_file()
    except AssertionError as e:
        if e == "Reached EOF.":
            print "ERROR: Reached End Of File."
    d.close()
    elapsed_time = time.time() - start_time
    print args.compressed_filename, "decode_python - elapsed time =", round(elapsed_time, 2), "seconds"


def code_decode_python(args):
    coder_info, columns_bits = code_python(args)
    decode_python(args)
    return [coder_info, columns_bits]


def compress_file(args):
    print args.coder_params
    coder_info, columns_bits = code_python(args)
    py_filename = args.compressed_filename
    code_cpp(args)
    cpp_filename = args.compressed_filename
    print "Comparing compressed files..."
    assert(BitStreamUtils.compare_files(args.output_path, py_filename, args.output_path, cpp_filename))

    decode_python(args)
    py_filename = args.deco_filename
    decode_cpp(args)
    cpp_filename = args.deco_filename
    print "Comparing decompressed files..."
    assert(BitStreamUtils.compare_files(args.output_path, py_filename, args.output_path, cpp_filename))
    assert(BitStreamUtils.compare_files(args.input_path, args.input_filename, args.output_path, cpp_filename))
    same_file = True
    # assert(1 == 0)
    # csv_compare = CSVCompare(args.input_path, args.input_filename, args.output_path, cpp_filename)
    # same_file = csv_compare.compare(args.coder_params.get('error_threshold'))
    # assert same_file

    # if args.coder in PYTHON_CODERS:
    #     coder_info, columns_bits = code_decode_python(args)
    # else:
    #     coder_info, columns_bits = code_decode_cpp(args)

    # compare
    # csv_compare = CSVCompare(args.input_path, args.input_filename, args.output_path, args.deco_filename)
    # same_file = csv_compare.compare(args.coder_params.get('error_threshold'))
    # assert same_file

    # print results
    input_file = args.input_path + "/" + args.input_filename
    compressed_file = args.output_path + "/" + args.compressed_filename
    compressed_size = print_results(coder_info, args.logger, input_file, compressed_file, same_file)
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


def script(output_filename):
    datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/"
    # datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/results/paper_csv/3-without-outliers/"
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/"
    # output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/paper-output/"

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
    row_count = PrintUtils.separate(CSVUtils.csv_row_count(input_path, input_filename))

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

    coder_name = coder_dictionary['coder'].name()
    # CoderBasic - no params
    if coder_name == 'CoderBasic':
        values = [coder_name] + [None] * 3
        args = {
            'logger': logger,
            'coder': coder_dictionary['coder'],
            'coder_params': {},
            'decoder': coder_dictionary['decoder'],
            'input_path': input_path,
            'input_filename': input_filename,
            'output_path': output_dataset_coder_path
        }
        compress_args = CompressArgs(args)
        compression_values = compress_file(compress_args)
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
                values = [coder_name] if id3 == 0 and id4 == 0 else [None]
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
                compress_args = CompressArgs(args)
                compression_values = compress_file(compress_args)
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
