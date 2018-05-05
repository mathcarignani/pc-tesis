import os

import sys
sys.path.append('.')

from aux.logger import setup_logger
from scripts.utils import create_folder
from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.csv_utils.csv_writer import CSVWriter


dataset_hash = {
    'CO2': 0,  # integer
    'Humidity': 2,  # 17,
    'Lysimeter': 2,
    'Moisture': 2,  # 16,
    'Pressure': 1,
    'Radiation': 2,  # 15,
    'Snow_height': 2,  # 6,
    'Temperature': 2,  # 17,
    'Voltage': 2,  # 17,
    'Wind_direction': 2,  # 14,
    'Wind_speed': 2  # 16
}

outliers = {
    'CO2': {
        'co2_10.csv': ['32307'], 'co2_11.csv': ['32307'], 'co2_9.csv': ['32307']
    },
    'Humidity': {
        'humidity_11.csv': ['824'], 'humidity_15.csv': ['008'], 'humidity_17.csv': ['8'],
        'humidity_34.csv': ['-32768.0'], 'humidity_6.csv': ['183'], 'humidity_7.csv': ['896'],
        'humidity_9.csv': ['355']
    },
    'Lysimeter': {},
    'Moisture': {
        'moisture_12.csv': ['72'], 'moisture_17.csv': ['000000001']
    },
    'Pressure': {},
    'Radiation': {
        'radiation_18.csv': ['596806387'], 'radiation_27.csv': ['260555811'], 'radiation_29.csv': ['997718848'],
        'radiation_30.csv': ['8167'], 'radiation_32.csv': ['236515979']
    },
    'Snow_height': {},
    'Temperature': {
        'temperature_15.csv': ['35'], 'temperature_16.csv': ['75'], 'temperature_17.csv': ['75'],
        'temperature_20.csv': ['63'], 'temperature_23.csv': ['55'], 'temperature_28.csv': ['35'],
        'temperature_32.csv': ['285'], 'temperature_42.csv': ['63'], 'temperature_52.csv': ['9999999998']
    },
    'Voltage': {
        'voltage_13.csv': ['9'], 'voltage_14.csv': ['6'],  # 'voltage_4.csv': ['15'] => not an outlier
    },
    'Wind_direction': {
        'wind_direction_1.csv': ['765280077'], 'wind_direction_19.csv': ['026024718'],
        'wind_direction_25.csv': ['59585489'], 'wind_direction_29.csv': ['601127276'],
        'wind_direction_30.csv': ['838423745'], 'wind_direction_31.csv': ['102797498'],
        'wind_direction_33.csv': ['912957697'],
        'wind_direction_34.csv': ['423439279']
    },
    'Wind_speed': {
        'wind_speed_10.csv': ['04166666667'], 'wind_speed_40.csv': ['667'],
        'wind_speed_44.csv': ['5833333333'], 'wind_speed_45.csv': ['0208333333'],
        'wind_speed_7.csv': ['2916666667'], 'wind_speed_9.csv': ['6667']
    }
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

    size, bit_length = calculate_size_and_bit_length(min_, max_)
    logger.info("DATASET = %s, min=%s, max=%s, size=%s, bit_length=%s" % (folder, min_, max_, size, bit_length))
    logger.info("%s=[0,131071],[%s,%s]=17,%s" % (folder, min_, max_, bit_length))
    logger.info("")


def convert_datafile(folder, input_folder_path, filename, output_folder_path):
    input_file = TextFileReader(input_folder_path, filename)
    output_file = CSVWriter(output_folder_path, filename)

    output_file.write_row(['DATASET:', folder])
    output_file.write_row(['TIME UNIT:', 'hours'])  # doesn't matter
    output_file.write_row(['FIRST TIMESTAMP:', "2015-01-01 00:00:00"])  # doesn't matter
    output_file.write_row(['Time Delta', 'Value'])

    file_outliers = []
    if outliers.get(folder) and outliers.get(folder).get(filename):
        file_outliers = outliers[folder][filename]

    min_, max_, count = convert_rows(folder, input_file, output_file, file_outliers)
    size, bit_length = calculate_size_and_bit_length(min_, max_)
    logger.info("  %s, min=%s, max=%s, count=%s, size=%s, bit_length=%s" % (filename, min_, max_, count, size, bit_length))
    return [min_, max_]


def convert_rows(folder, input_file, output_file, file_outliers):
    data_after_comma = dataset_hash[folder]

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

        if line in file_outliers:
            logger.info("OUTLIER. count = %s => %s" % (count, line))
            continue

        print_info = False

        if data_after_comma == 0:  # integer
            if "." in line:
                logger.info(". count = %s => %s" % (count, line))
                raise StandardError()
            value = int(line)

        else:  # data_after_comma > 0
            if "." not in line and folder != 'Pressure':
                print_info = True

            value = float(line)
            value = int(value * 10 ** data_after_comma)

        output_file.write_row([0, value])

        if min_ is None:  # and max_ is None
            min_, max_ = value, value
        elif value < min_:
            min_ = value
            if print_info:
                logger.info("new MIN missing .: count = %s => %s" % (count, line))
        elif value > max_:
            max_ = value
            if print_info:
                logger.info("new MAX missing .: count = %s => %s" % (count, line))
        count += 1
    return [min_, max_, count]


def calculate_size_and_bit_length(min_, max_):
    size = max_ - min_ + 1 if max_ >= 0 else -max_ - min_ + 1
    return [size, size.bit_length()]

run()
