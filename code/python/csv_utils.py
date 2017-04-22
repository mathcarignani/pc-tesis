import csv
import numpy as np
from progress import print_progress

def clean_row(row, keep_columns, remove_columns):
		if len(keep_columns) > 0:
				return np.keep(row, keep_columns)
		elif len(remove_columns) > 0:
				return np.delete(row,remove_columns)
		else:
				return row

# This method is used for removing columns of a csv file
def clean_csv(read_filename, write_filename, keep_columns=[], remove_columns=[], number_rows=None):
		with open(write_filename, 'wb') as w:
		    writer = csv.writer(w)

		    with open(read_filename, 'rb') as r:
		    	reader = csv.reader(r)
		    	total_rows = len(list(reader))
		    	if (number_rows is not None) and (number_rows < total_rows):
		    			total_rows = number_rows

		    	r.seek(0)
		    	current_row = 0

		    	for row in reader:
		    		if current_row < total_rows:
				    		new_row = clean_row(row, keep_columns, remove_columns)
				    		writer.writerow(new_row)

				    		current_row += 1
				    		if (current_row % 1000 == 0) or (current_row == total_rows):
				    				print_progress(current_row, total_rows)

def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1

def update_res_array(res_array, row):
		for i in range(len(row)):
				if row[i] == None:
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
							for _ in range(len(row)):
									res_array.append({'count': 0, 'sum': 0, 'min': None, 'max': None, 'decimals': None})

					if current_row > 0: # column names
						update_res_array(res_array, row)

					current_row += 1
					if (current_row % 1000 == 0) or (current_row == total_rows):
							print_progress(current_row, total_rows)

				for i in range(len(res_array)):
						print res_array[i]






clean_csv('../../datasets/el-nino/elnino.csv', 'elnino-clean.csv', remove_columns=[0,4,7,8,9], number_rows=10)

csv_stats('elnino-clean.csv')