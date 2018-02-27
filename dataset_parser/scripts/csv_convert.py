import logging

import sys
sys.path.append('.')

from aux.date_range import DateRange
from aux.logger import Logger
from csv_converter.csv_converter import CSVConverter
from csv_converter.csv_converter_noaa import CSVConverterNOAA
from csv_converter.csv_converter_adcp import CSVConverterADCP
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.text_utils.text_file_reader import TextFileReader

from parsers.adcp.parser_adcp import ParserADCP
from parsers.climaps.parser_climaps import ParserClimaps
from parsers.elnino.parser_elnino import ParserElNino
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA
from parsers.solar_anywhere.parser_solar_anywhere import ParserSolarAnywhere



import os
current_path = os.path.dirname(os.path.abspath(__file__))
datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/"


def convert_to_csv(parser_klass, input_path, input_filenames, output_path, reader_cls, date_range):
    for input_filename in input_filenames:
        output_filename = input_filename + '.csv'
        logging.info("#################################################################################")
        logging.info("INPUT: %s/%s", input_path, input_filename)
        logging.info("OUTPUT: %s/%s", output_path, output_filename)
        input_file = reader_cls(input_path, input_filename)
        csv_converter = CSVConverter(parser_klass())
        csv_converter.input_csv_to_df(input_file, date_range)
        csv_converter.print_stats()
        csv_converter.df_to_output_csv(output_path, output_filename)
        csv_converter.plot(output_path)


def convert_to_csv_noaa(csv_converter, input_path, input_filenames, output_path, reader_cls, output_filename, date_range=DateRange()):
    for input_filename in input_filenames:
        logging.info("#################################################################################")
        logging.info("INPUT: %s/%s", input_path, input_filename)
        input_file = reader_cls(input_path, input_filename)
        csv_converter.input_csv_to_df(input_file, date_range)
    csv_converter.df_to_output_csv(output_path, output_filename)


def run(parser_klass, logger_filename, input_folder, output_folder, reader_cls=TextFileReader, date_range=DateRange()):
    Logger.set(logger_filename)
    input_path = datasets_path + input_folder
    input_filenames = os.listdir(input_path)
    output_path = current_path + output_folder
    if parser_klass == ParserNOAA:
        convert_to_csv_noaa(CSVConverterNOAA(), input_path, input_filenames, output_path, reader_cls, 'noaa2017.csv', date_range)
    elif parser_klass == ParserADCP:
        convert_to_csv_noaa(CSVConverterADCP(), input_path, input_filenames, output_path, reader_cls, 'adcp2017.csv', date_range)
    else:
        convert_to_csv(parser_klass(), input_path, input_filenames, output_path, reader_cls, date_range)


# [1]irkis
# run(ParserVWC, "output-irkis.log", "[1]irkis/vwc", "/[1]irkis")

# [2]noaa-buoy
# date_range = DateRange('01/01/2017 00:00', None)
# run(ParserNOAA, "output-noaa-buoy.log", "[2]noaa-buoy/17-2808.tar", "/[2]noaa-buoy/2017", TextFileReader, date_range)

# [3]noaa-adcp
date_range = DateRange('01/01/2014 00:00', '01/02/2014 00:00')
run(ParserADCP, "output-noaa-adcp.log", "[3]noaa-adcp/test", "/[3]noaa-adcp/2017", TextFileReader, date_range)


# run(ParserElNino, "output-elnino.log", "[3]el-nino/large/data", "/[3]el-nino")
# run(ParserSolarAnywhere, "output-solar-anywhere.log", "[4]solar-anywhere/2/data", "/[4]solar-anywhere", CSVReader)
# run(ParserClimaps, "output-climaps.log", "[5]climaps/crete/17/climaps-data", "/[5]climaps", CSVReader)
