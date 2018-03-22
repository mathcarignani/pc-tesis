import sys
sys.path.append('.')
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

import os


def change_csv_names():
    # dataset_path = csv_path + '/' + dataset_folder
    dataset_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[2]noaa-sst/months/2017"
    input_filenames = os.listdir(dataset_path)
    input_filenames = [f for f in input_filenames if os.path.isfile(os.path.join(dataset_path, f))]
    input_filenames = [f for f in input_filenames if f.endswith(".csv")]
    for filename in input_filenames:
        old_name = dataset_path + '/' + filename
        new_name = dataset_path + '/' + filename.replace(".csv", ".old.csv")
        print old_name, new_name
        os.rename(old_name, new_name)


def modify_csv(path, old_file):
    input_file = CSVReader(path, old_file)
    output_file = CSVWriter(path, old_file.replace(".old.csv", ".csv"))
    print "FILE AND SIZE", input_file.full_path, str(input_file.total_lines)

    first_rows(input_file, output_file)
    while input_file.continue_reading:
        row = input_file.read_line()
        new_row = create_new_row(row)
        output_file.write_row(new_row)
    input_file.close()
    output_file.close()


def first_rows(input_file, output_file):
    output_file.write_row(['DATASET:', 'NOAA-SST'])  # DATASET:| IRKIS
    output_file.write_row(['TIME UNIT:', 'seconds'])  # TIME UNIT:| minutes

    row1, row2 = input_file.read_line(), input_file.read_line()

    row3, row4 = input_file.read_line(), input_file.read_line()
    output_file.write_row(['FIRST TIMESTAMP:', row3[1]])  # FIRST TIMESTAMP:| 2010-10-01 00:00:00

    output_file.write_row(remove_commas(row4))

    # row[0] = "Time Delta"
    # output_file.write_row(remove_commas(row3))  # Min Delta|Col1|Col2| ... |ColN

    # row4[0] = "0"
    # output_file.write_row(remove_commas(row4))


def remove_commas(row):
    new_row = [value.split('.')[0] for value in row]
    new_row = [value.split('000')[0] for value in new_row]
    return new_row


def create_new_row(row):
    new_delta = convert_to_minutes(row[0])
    new_row = [new_delta] + row[1:]
    new_row = remove_commas(new_row)
    return new_row


def convert_to_minutes(delta):
    return str(int(delta)*60)
    # hours, minutes, seconds = delta.split(':')
    # return str(60*60*int(hours) + 60*int(minutes) + int(seconds))

    # if seconds != '00':
    #     raise "SECONDS MUST BE '00'!!"
    # else:
    #     return str(60*int(hours) + int(minutes))


def run_script(dataset_folder):
    dataset_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/" + dataset_folder
    input_filenames = os.listdir(dataset_path)
    input_filenames = [f for f in input_filenames if os.path.isfile(os.path.join(dataset_path, f))]
    input_filenames = [f for f in input_filenames if f.endswith(".old.csv")]
    # print input_filenames
    for input_filename in input_filenames:
        modify_csv(dataset_path, input_filename)


# run_script('[1]irkis')
run_script('[2]noaa-sst/months/2017')
# run_script('[4]solar-anywhere/2011')
# run_script('[4]solar-anywhere/2012')
# run_script('[4]solar-anywhere/2013')
# run_script('[4]solar-anywhere/2014')

