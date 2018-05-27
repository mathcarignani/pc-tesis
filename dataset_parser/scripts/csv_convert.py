from calendar import monthrange

import sys
sys.path.append('.')

from aux.date_range import DateRange
from aux.logger import setup_logger
from csv_converter.csv_converter import CSVConverter
from csv_converter.csv_converter_noaa import CSVConverterNOAA
from csv_converter.csv_converter_adcp import CSVConverterADCP
from csv_converter.csv_converter_solar_anywhere import CSVConverterSolarAnywhere
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.text_utils.text_file_reader import TextFileReader

from parsers.adcp.parser_adcp import ParserADCP
# from parsers.climaps.parser_climaps import ParserClimaps
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA
from parsers.noaa_spc.parser_noaa_spc import ParserNOAASPC
from parsers.solar_anywhere.parser_solar_anywhere import ParserSolarAnywhere


import os
current_path = os.path.dirname(os.path.abspath(__file__))
datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/"


def convert_to_csv_many(args, csv_converter, input_path, input_filenames, output_path, plot_output_path=None):
    logger = args['logger']
    reader_cls = args['reader_cls']
    for input_filename in input_filenames:
        logger.info("#################################################################################")
        logger.info("INPUT: %s/%s", args['input_path'], input_filename)

        input_file = reader_cls(input_path, input_filename)
        if plot_output_path is None:
            csv_converter.input_csv_to_df(input_file, args['date_range'])
        else:
            csv_converter.input_csv_to_df(input_file, args['date_range'], plot_output_path)
    csv_converter.df_to_output_csv(output_path, args['output_filename'])
    csv_converter.print_stats()


def run(args):
    input_path = datasets_path + args['input_path']
    input_filenames = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
    output_path = current_path + args['output_path']
    parser_cls = args['parser_cls']
    logger = args['logger']
    if parser_cls == ParserNOAA:
        convert_to_csv_many(args, CSVConverterNOAA(logger), input_path, input_filenames, output_path)
    elif parser_cls == ParserADCP:
        convert_to_csv_many(args, CSVConverterADCP(logger), input_path, input_filenames, output_path)
    elif parser_cls == ParserSolarAnywhere:
        convert_to_csv_many(args, CSVConverterSolarAnywhere(logger), input_path, input_filenames, output_path, output_path)


def noaa_buoy(year, month=None):
    if month is None:
        first, last = "01/01/%s 00:00" % year, "12/31/%s 23:59" % year
        logger_filename = "output-noaa-buoy-%s.log" % year
        output_filename = "noaa-buoy-%s.csv" % year
    else:
        first = "%s/01/%s 00:00" % (month, year)
        last_day_month = monthrange(year, month)[1]
        last = "%s/%s/%s 23:59" % (month, last_day_month, year)
        month_s = str(month) if month > 9 else '0' + str(month)
        logger_filename = "output-noaa-buoy-%s%s.log" % (year, month_s)
        output_filename = "noaa-buoy-%s%s.csv" % (year, month_s)
    date_range = DateRange(first, last)
    logger = setup_logger(logger_filename, logger_filename)
    args = {
        'parser_cls': ParserNOAA,
        'logger': logger,
        'date_range': date_range,
        'reader_cls': TextFileReader,
        'input_path': "[2]noaa-sst/17-2808.tar",
        'output_path': "/[2]noaa-buoy",
        'output_filename': output_filename
    }
    run(args)

# noaa_buoy(2009)
# for month in reversed(range(1, 13)):
#     noaa_buoy(2017, month)


def noaa_adcp(year, month=None):
    if month is None:
        first, last = "01/01/%s 00:00" % year, "12/31/%s 23:59" % year
        logger_filename = "output-noaa-adcp-%s.log" % year
        output_filename = "noaa-adcp-%s.csv" % year
    else:
        first = "%s/01/%s 00:00" % (month, year)
        last_day_month = monthrange(year, month)[1]
        last = "%s/%s/%s 23:59" % (month, last_day_month, year)
        month_s = str(month) if month > 9 else '0' + str(month)
        logger_filename = "output-noaa-adcp-%s%s.log" % (year, month_s)
        output_filename = "noaa-adcp-%s%s.csv" % (year, month_s)
    date_range = DateRange(first, last)
    logger = setup_logger(logger_filename, logger_filename)
    args = {
        'parser_cls': ParserADCP,
        'logger': logger,
        'date_range': date_range,
        'reader_cls': TextFileReader,
        'input_path': "[3]noaa-adcp/d27-190.tar",
        'output_path': "/[3]noaa-adcp",
        'output_filename': output_filename
    }
    run(args)

# for year in reversed(range(2012, 2016)):
#     noaa_adcp(year)


def solar_anywhere(year, month=None):
    if month is None:
        first, last = "01/01/%s 00:00" % year, "12/31/%s 23:59" % year
        logger_filename = "solar-anywhere-%s.log" % year
        output_filename = "solar-anywhere-%s.csv" % year
    else:
        first = "%s/01/%s 00:00" % (month, year)
        last_day_month = monthrange(year, month)[1]
        last = "%s/%s/%s 23:59" % (month, last_day_month, year)
        month_s = str(month) if month > 9 else '0' + str(month)
        logger_filename = "solar-anywhere-%s%s.log" % (year, month_s)
        output_filename = "solar-anywhere-%s%s.csv" % (year, month_s)
    date_range = DateRange(first, last)
    logger = setup_logger(logger_filename, logger_filename)
    args = {
        'parser_cls': ParserSolarAnywhere,
        'logger': logger,
        'date_range': date_range,
        'reader_cls': CSVReader,
        'input_path': "[4]solar-anywhere/2011",
        'output_path': "/[4]solar-anywhere",
        'output_filename': output_filename
    }
    run(args)

# solar_anywhere(2011)


def noaa_spc(dataset):
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/[6]noaa-spc-reports"
    input_filename = "noaa_spc." + dataset + "_reports.csv"
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/[6]noaa-spc-reports"
    logger_filename = "noaa_spc-" + dataset + ".log"
    output_filename = "noaa_spc-" + dataset + ".csv"

    logger = setup_logger(logger_filename, logger_filename)
    if dataset == 'tornado':
        input_file = CSVReader(input_path, input_filename, False, '\t')
    else:
        input_file = CSVReader(input_path, input_filename)

    parser = ParserNOAASPC(logger, dataset)
    csv_converter = CSVConverter(parser, logger)
    csv_converter.input_csv_to_df(input_file, None, None, False, True)
    csv_converter.df_to_output_csv(output_path, output_filename)
    csv_converter.print_stats()

    input_file.close()

# noaa_spc('hail')
# noaa_spc('tornado')
# noaa_spc('wind')

# def compare():
#     path1 = "/Users/pablocerve/Documents/FING/Proyecto/datasets/[6]noaa-spc-reports"
#     filename1 = "noaa_spc.wind_reports.csv"
#     path2 = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/[6]noaa-spc-reports"
#     filename2 = "noaa_spc-wind.csv"
#
#     file1 = CSVReader(path1, filename1)
#     file2 = CSVReader(path2, filename2)
#
#     file1.goto_row(1)
#     file2.goto_first_data_row()
#
#     count = 0
#     while file1.continue_reading:
#         row1 = file1.read_line()
#         row2 = file2.read_line()
#         lat1, long1, speed1 = int(float(row1[7])*100), int(float(row1[8])*100), int(row1[2])
#         row2 = row2[1:]
#         lat2, long2, speed2 = [int(i) for i in row2]
#
#         if lat1 != lat2 or long1 != long2 or speed1 != speed2:
#             print 'count', count
#             print row1
#             print row2
#             break
#         count += 1
#     print count
