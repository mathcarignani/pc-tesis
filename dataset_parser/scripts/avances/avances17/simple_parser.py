# TODO: remove this file

import sys
sys.path.append('.')

from file_utils.text_utils.text_file_reader import TextFileReader

path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/avances/avances17"
filename = "input.txt"

reader = TextFileReader(path, filename)
min_value, max_value, current_filename, current_coder = 0, 0, "", ""
current_pdf = ""


def print_values(min_value, max_value):
    if min_value < 0:
        print 'min_value = ' + str(min_value)
    if max_value > 0:
        print 'max_value = ' + str(max_value)


def update_min_value(value, min_value):
    return value if value < min_value else min_value


def update_max_value(value, max_value):
    return value if value > max_value else max_value


def parse_value(line):
    return float(line.split()[2])


while reader.continue_reading:
    line = reader.read_line()

    if "pdf" in line:
        print_values(min_value, max_value)
        min_value, max_value, current_filename, current_coder = 0, 0, "", ""
        current_pdf = line.strip('\n')
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + current_pdf
        first = True
    if current_pdf == "pdf1" and "FILENAME" in line:
        # FILENAME = el-nino.csv - COLUMN_INDEX = 2
        new_filename = line.split()[2]
        if new_filename != current_filename:
            if not first:
                print_values(min_value, max_value)
            first = False
            print new_filename
            min_value, max_value, current_filename = 0, 0, new_filename
    if "min_value" in line or "max_value" in line:
        # min_value = -1.10145781181
        # max_value = 19.5591527467
        value = parse_value(line)
        min_value = update_min_value(value, min_value)
        max_value = update_max_value(value, max_value)

print_values(min_value, max_value)

reader.close()
