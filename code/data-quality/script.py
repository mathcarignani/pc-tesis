from file_reader import FileReader
from parser_vwc import ParserVWC
from parser_smet import ParserSMET
import sys

# EXAMPLE USAGE:
# python script.py vwc /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/vwc
# python script.py station /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/station
# python script.py interpolatedmeteo /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/interpolatedmeteo

def parse_vwc_files(folder):
	filenames = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]
	for filename in filenames:
		parser = ParserVWC()
		_parse_and_process(parser, folder, filename)
		parser.plot()
		print

def parse_smet_files(key, folder):
	# station_ids = ["1202", "1203", "1204", "1205", "222", "333", "SLF2"]
	station_ids = ["222", "333", "SLF2"]
	for station_id in station_ids:
		filename = key + "_" + station_id + ".smet"
		_parse_and_process(ParserSMET(), folder, filename)
		print

def _parse_and_process(parser, folder, filename):
	file_reader = FileReader(folder, filename)
	file_reader.parse_file(parser)
	parser.process_data()

args = sys.argv[1:]
if len(args) != 2:
	print "ERROR: Missing script parameter."
	print "Correct usages:"
	print "(1) python script.py vwc /folder/path/to/files"
	print "(2) python script.py station /folder/path/to/files"
	print "(3) python script.py interpolatedmeteo /folder/path/to/files"
elif args[0] == 'vwc':
	parse_vwc_files(args[1])
elif args[0] == 'station' or args[0] == 'interpolatedmeteo':
	parse_smet_files(args[0], args[1])
