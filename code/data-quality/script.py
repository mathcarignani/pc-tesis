from smet_reader import *
import time

folder = "/media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/interpolatedmeteo"
station_ids = ["222", "333", "1202", "1203", "1204", "1205", "SLF2"]

for station_id in station_ids:
	filename = "interpolatedmeteo_" + station_id + ".smet"
	smet_reader = SMETReader(folder, filename)
	start = time.time()
	df = smet_reader.parse_file()
	print
	end = time.time()
	elapsed = end - start
	print "Time elapsed:", elapsed, "sec"
	print df.describe()