from data import *
from smet_reader import *
from vwc_reader import *
from repeat_finder import *
import time

parent_folder = "/media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/"
# folder_names = ["station", interpolatedmeteo"]
# station_ids = ["1202", "1203", "1204", "1205", "222","333", "SLF2"]

# for folder_name in folder_names:
# 	folder = parent_folder + folder_name
# 	for station_id in station_ids:
# 		filename = folder_name + "_" + station_id + ".smet"
# 		smet_reader = SMETReader(folder, filename)
# 		start = time.time()
# 		data = smet_reader.parse_file()
# 		print
# 		end = time.time()
# 		elapsed = end - start
# 		print "Time elapsed:", elapsed, "sec"
# 		data.post_parsing()
# 		data.analize()


filenames = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]
folder_name = "vwc"
folder = parent_folder + folder_name
for filename in filenames:
	vwc_reader = VWCReader(folder, filename)
	start = time.time()
	data = vwc_reader.parse_file()
	print
	end = time.time()	
	elapsed = end - start
	print "Time elapsed:", elapsed, "sec"
	data.post_parsing()
	data.analize()

# folder_name = "vwc"
# filenames = ["vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_222.smet", "vwc_333.smet", "vwc_SLF2.smet"]
# folder_name = "station"
# filenames = ["station_1202.smet", "station_1203.smet", "station_1204.smet", "station_1205.smet",
# 							"station_222.smet", "station_333.smet", "station_SLF2.smet"]
# folder_name = "interpolatedmeteo"
# filenames = ["interpolatedmeteo_1202.smet", "interpolatedmeteo_1203.smet", "interpolatedmeteo_1204.smet", "interpolatedmeteo_1205.smet",
# 							"interpolatedmeteo_222.smet", "interpolatedmeteo_333.smet", "interpolatedmeteo_SLF2.smet"]
# folder = parent_folder + folder_name
# for filename in filenames:
# 	repeat_finder = RepeatFinder(folder, filename)
# 	start = time.time()
# 	data = repeat_finder.parse_file()
# 	print
# 	end = time.time()
# 	elapsed = end - start
# 	print "Time elapsed:", elapsed, "sec"
