import sys
sys.path.append('.')

from aux.date_range import DateRange
from aux.logger import setup_logger
from csv_converter.csv_converter import CSVConverter
from csv_converter.csv_converter_noaa import CSVConverterNOAA
from csv_converter.csv_converter_adcp import CSVConverterADCP
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.text_utils.text_file_reader import TextFileReader

from parsers.adcp.parser_adcp import ParserADCP
# from parsers.climaps.parser_climaps import ParserClimaps
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


def convert_to_csv_noaa(args, csv_converter, input_path, input_filenames, output_path):
    logger = args['logger']
    reader_cls = args['reader_cls']
    for input_filename in input_filenames:
        logger.info("#################################################################################")
        logger.info("INPUT: %s/%s", args['input_path'], input_filename)

        input_file = reader_cls(input_path, input_filename)
        csv_converter.input_csv_to_df(input_file, args['date_range'])
    csv_converter.df_to_output_csv(output_path, args['output_filename'])
    csv_converter.print_stats()


def run(args):
    input_path = datasets_path + args['input_path']
    input_filenames = os.listdir(input_path)
    output_path = current_path + args['output_path']
    parser_cls = args['parser_cls']
    logger = args['logger']
    if parser_cls == ParserNOAA:
        convert_to_csv_noaa(args, CSVConverterNOAA(logger), input_path, input_filenames, output_path)
    elif parser_cls == ParserADCP:
        convert_to_csv_noaa(args, CSVConverterADCP(logger), input_path, input_filenames, output_path)
    else:
        convert_to_csv(parser_cls(), input_path, input_filenames, output_path, reader_cls, date_range)


def irkis():
    run(ParserVWC, "output-irkis.log", "[1]irkis/vwc", "/[1]irkis")


def noaa_buoy(year):
    first, last = "01/01/%s 00:00" % year, "12/31/%s 23:59" % year
    date_range = DateRange(first, last)
    logger_filename = "output-noaa-buoy-%s.log" % year
    logger = setup_logger(logger_filename, logger_filename)
    args = {
        'parser_cls': ParserNOAA,
        'logger': logger,
        'date_range': date_range,
        'reader_cls': TextFileReader,
        'input_path': "[2]noaa-buoy/17-2808.tar",
        'output_path': "/[2]noaa-buoy",
        'output_filename': "noaa-buoy-%s.csv" % year
    }
    run(args)


def noaa_adcp():
    date_range = DateRange('01/01/2014 00:00', '01/31/2014 23:59')
    run(ParserADCP, "output-noaa-adcp.log", "[3]noaa-adcp/d27-190.tar", "/[3]noaa-adcp/2014", TextFileReader, date_range)


# run(ParserElNino, "output-elnino.log", "[3]el-nino/large/data", "/[3]el-nino")
# run(ParserSolarAnywhere, "output-solar-anywhere.log", "[4]solar-anywhere/2/data", "/[4]solar-anywhere", CSVReader)
# run(ParserClimaps, "output-climaps.log", "[5]climaps/crete/17/climaps-data", "/[5]climaps", CSVReader)


for year in reversed(range(2000, 2018)):
    noaa_buoy(year)
