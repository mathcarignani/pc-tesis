import os

import sys
sys.path.append('.')

from aux.logger import setup_logger
from scripts.utils import create_folder
from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.csv_utils.csv_writer import CSVWriter


dataset_hash = {
    'CO2': {'type': 'int'},
    'Humidity': {'type': 'float', 'after_comma': 17},
    'Lysimeter': {'type': 'float', 'after_comma': 2},
    'Moisture': {'type': 'float', 'after_comma': 16},
    'Pressure': {'type': 'float', 'after_comma': 1},
    'Radiation': {'type': 'float', 'after_comma': 15},
    'Snow_height': {'type': 'float', 'after_comma': 6},
    'Temperature': {'type': 'float', 'after_comma': 17},
    'Voltage': {'type': 'float', 'after_comma': 17},
    'Wind_direction': {'type': 'float', 'after_comma': 14},
    'Wind_speed': {'type': 'float', 'after_comma': 16}
}

run_list = []
logger = setup_logger("convert_paper_datasets.log", "convert_paper_datasets.log")


def run():
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/simulator/Normalized data"
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/paper_csv"
    for folder in os.listdir(input_path):
        # if folder not in run_list:
        #     continue
        output_folder_path = os.path.join(output_path, folder)
        create_folder(output_folder_path)

        input_folder_path = os.path.join(input_path, folder)
        convert_dataset(folder, input_folder_path, output_folder_path)


def convert_dataset(folder, input_folder_path, output_folder_path):
    min_, max_ = None, None
    logger.info(input_folder_path)
    for filename in os.listdir(input_folder_path):
        # print filename
        # if filename != 'humidity_4.csv':
        #     continue
        min__, max__ = convert_datafile(folder, input_folder_path, filename, output_folder_path)
        min_ = min__ if min_ is None or min__ < min_ else min_
        max_ = max__ if max_ is None or max__ > max_ else max_

    size = max_ - min_ + 1 if max_ >= 0 else -max_ - min_ + 1
    logger.info("DATASET = %s, min=%s, max=%s, size=%s, bit_length=%s" % (folder, min_, max_, size, size.bit_length()))
    logger.info("")


def convert_datafile(folder, input_folder_path, filename, output_folder_path):
    input_file = TextFileReader(input_folder_path, filename)
    output_file = CSVWriter(output_folder_path, filename)

    output_file.write_row(['DATASET:', filename])
    output_file.write_row(['TIME UNIT:', 'hours'])  # doesn't matter
    output_file.write_row(['FIRST TIMESTAMP:', "2015-01-01 00:0:00"])  # doesn't matter
    output_file.write_row(['Time Delta:', 'Value'])

    min_, max_, count = convert_rows(folder, input_file, output_file)
    logger.info("  %s, min=%s, max=%s, count=%s" % (filename, min_, max_, count))
    return [min_, max_]


def convert_rows(folder, input_file, output_file):
    data = dataset_hash[folder]
    min_, max_, count = None, None, None
    while input_file.continue_reading:
        line = input_file.read_line()
        line = line.rstrip('\r\n')

        if count is None:  # first line is always a comment
            assert("###" in line)
            count = 0
            continue

        if len(line) == 0:
            continue

        if data['type'] == 'int':
            if "." in line:
                logger.info(". %s %s" % (count, line))
                raise StandardError()
            value = int(line)

        else:  # data['type'] == 'float'
            if "." not in line:
                pass
                # print 'no .', count, line
            else:
                after_comma = line.split(".")[1]
                if len(after_comma) > data['after_comma']:
                    logger.info("%s %s %s" % (count, line, len(after_comma)))
                    raise StandardError()

            value = float(line)
            value = int(value * 10 ** data['after_comma'])

        output_file.write_row([0, value])
        min_ = value if min_ is None or value < min_ else min_
        max_ = value if max_ is None or value > max_ else max_
        count += 1
    return [min_, max_, count]

run()
