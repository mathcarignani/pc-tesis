import sys
from methods import parse_vwc_files, parse_smet_files

# EXAMPLE USAGE:
# python script.py vwc /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/vwc
# python script.py station /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/station
# python script.py interpolatedmeteo /media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/interpolatedmeteo

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
