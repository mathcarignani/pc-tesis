import logging
import datetime

import sys
sys.path.append('.')

from aux.logger import Logger
from csv_converter.csv_converter import CSVConverter
from csv_converter.csv_converter_noaa import CSVConverterNOAA
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


def convert_to_csv(parser_klass, input_path, input_filenames, output_path, reader_cls, lower_bound_date):
    for input_filename in input_filenames:
        output_filename = input_filename + '.csv'
        logging.info("#################################################################################")
        logging.info("INPUT: %s/%s", input_path, input_filename)
        logging.info("OUTPUT: %s/%s", output_path, output_filename)
        input_file = reader_cls(input_path, input_filename)
        csv_converter = CSVConverter(parser_klass())
        csv_converter.input_csv_to_df(input_file, lower_bound_date)
        csv_converter.print_stats()
        csv_converter.df_to_output_csv(output_path, output_filename)
        csv_converter.plot(output_path)


def convert_to_csv_noaa(input_path, input_filenames, output_path, reader_cls, lower_bound_date):
    csv_converter = CSVConverterNOAA()
    for input_filename in input_filenames:
        logging.info("#################################################################################")
        logging.info("INPUT: %s/%s", input_path, input_filename)
        input_file = reader_cls(input_path, input_filename)
        csv_converter.input_csv_to_df(input_file, lower_bound_date)
    csv_converter.df_to_output_csv(output_path, 'noaa2017.csv')


def run(parser_klass, logger_filename, input_folder, output_folder, reader_cls=TextFileReader, lower_bound_date=None):
    Logger.set(logger_filename)
    input_path = datasets_path + input_folder
    input_filenames = os.listdir(input_path)
    output_path = current_path + output_folder
    if parser_klass == ParserNOAA:
        convert_to_csv_noaa(input_path, input_filenames, output_path, reader_cls, lower_bound_date)
    else:
        convert_to_csv(parser_klass(), input_path, input_filenames, output_path, reader_cls, lower_bound_date)


# run(ParserVWC, "output-irkis.log", "[1]irkis/vwc", "/[1]irkis")
# run(ParserNOAA, "output-noaa.log", "[2]noaa/2016", "/[2]noaa")

lower_bound_date = datetime.datetime.strptime('30/12/2017', '%d/%m/%Y')
print lower_bound_date
run(ParserNOAA, "output-noaa-buoy.log", "[2]noaa/buoy/17-2808.tar", "/[3]noaa-buoy", TextFileReader, lower_bound_date)

# run(ParserElNino, "output-elnino.log", "[3]el-nino/large/data", "/[3]el-nino")
# run(ParserSolarAnywhere, "output-solar-anywhere.log", "[4]solar-anywhere/2/data", "/[4]solar-anywhere", CSVReader)
# run(ParserClimaps, "output-climaps.log", "[5]climaps/crete/17/climaps-data", "/[5]climaps", CSVReader)
