from file_reader import FileReader
from parser_noaa import ParserNOAA
# from file_writer import FileWriter
# from parser_vwc import ParserVWC
# from parser_smet import ParserSMET
# from cleaner_vwc import CleanerVWC

folder = "/Users/pablocerve/Documents/FING/Proyecto/datasets/noaa/1-d05-527.tar"
filename = "TAO_T0N95W_R_SST_10min.ascii"

parser = ParserNOAA()

def _parse_and_process(parser, folder, filename):
	file_reader = FileReader(folder, filename)
	file_reader.parse_file(parser)
	parser.process_data()

_parse_and_process(parser, folder, filename)


