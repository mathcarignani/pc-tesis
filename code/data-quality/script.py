from smet_reader import *
from data import *
import time

parent_folder = "/media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/"
folder_names = ["station"] # ["interpolatedmeteo", "station"]
station_ids = ["1202"] # ["222", "333", "1202", "1203", "1204", "1205", "SLF2"]

for folder_name in folder_names:
	folder = parent_folder + folder_name
	for station_id in station_ids:
		filename = folder_name + "_" + station_id + ".smet"
		smet_reader = SMETReader(folder, filename)
		start = time.time()
		data = smet_reader.parse_file()
		print
		end = time.time()
		elapsed = end - start
		print "Time elapsed:", elapsed, "sec"
		# print data.df.describe()
		# print data.df['RH'].head(n=5)
		data.post_parsing()
		data.analize()
		# print data.df['RH'].head(n=5)
		# print data.df.head(n=5)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++"
