import logging

import sys
sys.path.append('.')

from aux.logger import Logger
from csv_converter.csv_converter import CSVConverter
from file_utils.csv_utils.csv_reader import CSVReader
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA

import os
current_path = os.path.dirname(os.path.abspath(__file__))
datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/"


def convert_to_csv(parser_klass, input_path, input_filenames, output_path):
    row_count = None
    for input_filename in input_filenames:
        output_filename = input_filename + '.csv'
        logging.info("#################################################################################")
        logging.info("INPUT: %s/%s", input_path, input_filename)
        logging.info("OUTPUT: %s/%s", output_path, output_filename)
        csv_converter = CSVConverter(input_path, input_filename, parser_klass(), output_path, output_filename)
        csv_converter.run()
        csv_converter.print_stats()
        csv_converter.plot()
        csv_converter.close()

        count = CSVReader(output_path, output_filename).total_lines()
        if row_count is None:
            row_count = count
        elif row_count != count:
            logging.info("#### ERROR: row_count != count ### row_count=%s | count=%s", row_count, count)
        else:
            logging.info("SIZES MATCH!! count=%s", count)


def run(parser, logger_filename, input_folder, output_folder):
    Logger.set(logger_filename)
    input_path = datasets_path + input_folder
    input_filenames = os.listdir(input_path)
    output_path = current_path + output_folder
    convert_to_csv(parser, input_path, input_filenames, output_path)


run(ParserVWC, "output-irkis.log", "[1]irkis/vwc", "/irkis")
# run(ParserNOAA, "output-noaa.log", "[2]noaa/2016", "/noaa")
