import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.csv_utils.csv_reader import CSVReader

path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/results/3.1/06.2020/2-complete"

file = "results-mm3.csv"

new_file = "results-mm3-p.csv"

reader = CSVReader(path, file)
writer = CSVWriter(path, new_file)

while reader.continue_reading:
    line = reader.read_line()
    if "0" in line[4]:
        line[4] = int(float(line[4])*100)
    writer.write_row(line)

writer.close()
reader.close()