from file_utils.file_reader import FileReader
from file_utils.file_writer import FileWriter
from parser.parser_vwc import ParserVWC
from parser.parser_smet import ParserSMET
from data_quality.cleaner_vwc import CleanerVWC

VWC_FILES = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat",
             "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]


def parse_vwc_files(folder):
    for filename in VWC_FILES:
        parser = ParserVWC()
        _parse_and_process(parser, folder, filename)
        parser.plot(filename)
        print


def parse_smet_files(key, folder):
    station_ids = ["1202", "1203", "1204", "1205", "222", "333", "SLF2"]
    for station_id in station_ids:
        filename = key + "_" + station_id + ".smet"
        _parse_and_process(ParserSMET(), folder, filename)
        print


def _parse_and_process(parser, folder, filename):
    file_reader = FileReader(folder, filename)
    file_reader.parse_file(parser)
    parser.process_data()


def clean_vwc_files(input_folder, output_folder):
    for filename in VWC_FILES:
        # parse input file
        file_reader = FileReader(input_folder, filename)
        parser = ParserVWC()
        file_reader.parse_file(parser)
        # clean and write output file
        cleaner_vwc = CleanerVWC(parser.df, filename)
        file_writer = FileWriter(output_folder, cleaner_vwc.filename)
        cleaner_vwc.clean()
        file_writer.write_file(cleaner_vwc)
