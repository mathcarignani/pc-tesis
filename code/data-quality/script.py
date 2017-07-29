from file_reader import FileReader
from parser_vwc import ParserVWC
from parser_smet import ParserSMET
import sys

parent_folder = "/media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/"
station_ids = ["1202", "1203", "1204", "1205", "222","333", "SLF2"]

def parse_and_process(parser, folder, filename):
	file_reader = FileReader(folder, filename)
	file_reader.parse_file(parser)
	parser.process_data()

def parse_vwc_files():
	filenames = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]
	folder_name = "vwc"
	folder = parent_folder + folder_name
	for filename in filenames:
		parse_and_process(ParserVWC(), folder, filename)
		print

def parse_smet_files(folder_name, station_ids):
	folder = parent_folder + folder_name
	for station_id in station_ids:
		filename = folder_name + "_" + station_id + ".smet"
		parse_and_process(ParserSMET(), folder, filename)
		print

args = sys.argv[1:]
if len(args) == 0:
	print "ERROR: Missing script parameter."
	print "Correct usages:"
	print "python script.py vwc"
	print "python script.py station"
	print "python script.py interpolatedmeteo"
elif args[0] == 'vwc':
	parse_vwc_files()
elif args[0] == 'station':
	parse_smet_files('station')
elif args[0]:
	parse_smet_files('interpolatedmeteo')
