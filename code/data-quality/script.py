from file_reader import FileReader
from parser_vwc import ParserVWC
from parser_smet import ParserSMET
import sys

# EXAMPLE USAGE:
# python script.py vwc /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/vwc
# python script.py station /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/station
# python script.py interpolatedmeteo /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/interpolatedmeteo

def parse_and_process(parser, folder, filename):
	file_reader = FileReader(folder, filename)
	file_reader.parse_file(parser)
	parser.process_data()

def parse_vwc_files(folder):
	filenames = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]
	for filename in filenames:
		parse_and_process(ParserVWC(), folder, filename)
		print

def parse_smet_files(key, folder):
	station_ids = ["1202", "1203", "1204", "1205", "222","333", "SLF2"]
	for station_id in station_ids:
		filename = key + "_" + station_id + ".smet"
		parse_and_process(ParserSMET(), folder, filename)
		print

args = sys.argv[1:]
if len(args) != 2:
	print "ERROR: Missing script parameter."
	print "Correct usages:"
	print "(1) python script.py vwc folder_"
	print "(2) python script.py station"
	print "(3) python script.py interpolatedmeteo"
elif args[0] == 'vwc':
	parse_vwc_files(args[1])
elif args[0] == 'station' or args[0] == 'interpolatedmeteo':
	parse_smet_files(args[1], key)
