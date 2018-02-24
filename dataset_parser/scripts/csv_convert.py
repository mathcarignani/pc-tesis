import logging

import sys
sys.path.append('.')

from aux.logger import Logger
from csv_converter.csv_converter import CSVConverter
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.text_utils.text_file_reader import TextFileReader
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA
from parsers.elnino.parser_elnino import ParserElNino
from parsers.solar_anywhere.parser_solar_anywhere import ParserSolarAnywhere
from parsers.climaps.parser_climaps import ParserClimaps


import os
current_path = os.path.dirname(os.path.abspath(__file__))
datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/"


def convert_to_csv(parser_klass, input_path, input_filenames, output_path, reader_cls, year):
    # row_count = None
    for input_filename in input_filenames:
        output_filename = input_filename + '.csv'
        logging.info("#################################################################################")
        logging.info("INPUT: %s/%s", input_path, input_filename)
        logging.info("OUTPUT: %s/%s", output_path, output_filename)
        input_file = reader_cls(input_path, input_filename)
        csv_converter = CSVConverter(parser_klass())
        csv_converter.input_csv_to_df(input_file, year)
        csv_converter.print_stats()
        csv_converter.df_to_output_csv(output_path, output_filename)
        csv_converter.plot(output_path)

        # count = CSVReader(output_path, output_filename).total_lines()
        # if row_count is None:
        #     row_count = count
        # elif row_count != count:
        #     logging.info("#### ERROR: row_count != count ### row_count=%s | count=%s", row_count, count)
        # else:
        #     logging.info("SIZES MATCH!! count=%s", count)


def run(parser, logger_filename, input_folder, output_folder, reader_cls=TextFileReader, year=None):
    Logger.set(logger_filename)
    input_path = datasets_path + input_folder
    input_filenames = os.listdir(input_path)
    output_path = current_path + output_folder
    convert_to_csv(parser, input_path, input_filenames, output_path, reader_cls, year)


# run(ParserVWC, "output-irkis.log", "[1]irkis/vwc", "/[1]irkis")
# run(ParserNOAA, "output-noaa.log", "[2]noaa/2016", "/[2]noaa")

run(ParserNOAA, "output-noaa-buoy.log", "[2]noaa/buoy/17-2808.tar", "/[3]noaa-buoy", TextFileReader, 2013)
# run(ParserNOAA, "output-noaa-buoy.log", "[2]noaa/buoy/test", "/[3]noaa-buoy")

# run(ParserElNino, "output-elnino.log", "[3]el-nino/large/data", "/[3]el-nino")
# run(ParserSolarAnywhere, "output-solar-anywhere.log", "[4]solar-anywhere/2/data", "/[4]solar-anywhere", CSVReader)
# run(ParserClimaps, "output-climaps.log", "[5]climaps/crete/17/climaps-data", "/[5]climaps", CSVReader)
