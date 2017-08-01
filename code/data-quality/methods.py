from file_reader import FileReader
from parser_vwc import ParserVWC
from parser_smet import ParserSMET

def parse_vwc_files(folder):
	filenames = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat",
	  "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]
	for filename in filenames:
		parser = ParserVWC()
		_parse_and_process(parser, folder, filename)
		parser.plot(filename)
		print

def parse_smet_files(key, folder):
	# station_ids = ["1202", "1203", "1204", "1205", "222", "333", "SLF2"]
	station_ids = ["1203"]
	for station_id in station_ids:
		filename = key + "_" + station_id + ".smet"
		_parse_and_process(ParserSMET(), folder, filename)
		print

def _parse_and_process(parser, folder, filename):
	file_reader = FileReader(folder, filename)
	file_reader.parse_file(parser)
	parser.process_data()
