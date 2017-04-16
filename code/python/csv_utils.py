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


clean_csv('../../datasets/el-nino/elnino.csv', 'elnino-clean.csv', remove_columns=[0,4,7,8,9], number_rows=10)