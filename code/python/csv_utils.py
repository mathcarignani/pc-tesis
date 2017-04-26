import csv
import numpy as np
from progress import print_progress

def clean_row(row, keep_columns, remove_columns):
		if len(keep_columns) > 0:
				return np.take(row, keep_columns)
		elif len(remove_columns) > 0:
				return np.delete(row,remove_columns)
		else:
				return row

class ProcessRow:
		def __init__(self, total_rows, first_row, last_row):
				if (last_row is not None) and (last_row < total_rows):
						self.last_row = last_row
				else:
						self.last_row = total_rows
				if (first_row is not None) and (first_row < self.last_row):
						self.first_row = first_row
				else:
						self.first_row = 0

		def process_row(self, current_row):
				return (self.first_row <= current_row) and (current_row <= self.last_row)


# This method is used for removing columns of a csv file
def clean_csv(read_filename, write_filename, keep_columns=[], remove_columns=[], first_row=None, last_row=None):
		with open(write_filename, 'wb') as w:
		    writer = csv.writer(w)

		    with open(read_filename, 'rb') as r:
						reader = csv.reader(r)
						total_rows = len(list(reader))
						pr = ProcessRow(total_rows, first_row, last_row)

						r.seek(0)
						current_row = 0

						for row in reader:
								if pr.process_row(current_row):
										new_row = clean_row(row, keep_columns, remove_columns)
										writer.writerow(new_row)

								current_row += 1
								if (current_row % 1000 == 0) or (current_row == total_rows):
										print_progress(current_row, total_rows)

def compare_csv(filename1, filename2):
	with open(filename1, 'rb') as csvfile1:
	    with open (filename2, "rb") as csvfile2:
	        reader1 = csv.reader(csvfile1)
	        reader2 = csv.reader(csvfile2)

	        row_count = 0
	        for row1 in reader1:
	        		row2 = reader2.next()

	        		if row1==row2:
	        				row_count += 1
	        		else:
	        		 		print "diff csv, first diff row:", row_count
	        		 		return
	        print "same csv"
	        		


def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1

def update_res_array(res_array, row):
		for i in range(len(row)):
				if row[i] in [None, '.']:
						continue
				else:
						row_i = float(row[i])
						column_stats = res_array[i]
						column_stats['count'] += 1
						column_stats['sum'] += row_i

						if column_stats['min'] is None: # 'max' and 'decimals' are also None
								column_stats['min'] = row_i
								column_stats['max'] = row_i
								column_stats['decimals'] = num_after_point(row[i])
						else:
							if column_stats['min'] > row_i:
									column_stats['min'] = row_i
							if column_stats['max'] < row_i:
									column_stats['max'] = row_i	
							decimals = num_after_point(row[i])
							if decimals > column_stats['decimals']:
								column_stats['decimals'] = decimals

# This method returns the mean, max and min of every column in the csv file
def csv_stats(read_filename):
		with open(read_filename, 'rb') as r:
				reader = csv.reader(r)
				total_rows = len(list(reader))

				r.seek(0)
				current_row = 0
				res_array = []
				for row in reader:
					if current_row == 0:
							for i in range(len(row)):
									res_array.append({'column': row[i], 'count': 0, 'sum': 0, 'min': None, 'max': None, 'decimals': None})

					if current_row > 0: # column names
						update_res_array(res_array, row)

					current_row += 1
					if (current_row % 1000 == 0) or (current_row == total_rows):
							print_progress(current_row, total_rows)

				print total_rows - 1
				for i in range(len(res_array)):
						res = res_array[i]
						print res.pop('column')
						media = res['sum'] / res['count']
						media = round(media, res['decimals'])
						res['media'] = media
						print res



# clean_csv('../../datasets/el-nino/elnino.csv', 'elnino-clean.csv', keep_columns=[1,2,3], first_row=1)
# clean_csv('../../datasets/el-nino/elnino.csv', 'elnino-clean.csv', remove_columns=[0,4,7,8,9])
# csv_stats('elnino-clean.csv')

compare_csv('elnino-clean1.csv', 'elnino-clean1.csv.decoded.csv')
compare_csv('elnino-clean2.csv', 'elnino-clean2.csv.decoded.csv')
