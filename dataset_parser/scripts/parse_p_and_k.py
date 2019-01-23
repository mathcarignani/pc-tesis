import sys
sys.path.append('.')

from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.csv_utils.csv_writer import CSVWriter


def create_text_file_reader():
    path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-8"
    filename = "p,k.txt"
    return TextFileReader(path, filename)


def create_csv_writer():
    path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-8"
    filename = "p,k.csv"
    return CSVWriter(path, filename)


def script():
    text_file_reader = create_text_file_reader()
    csv_writer = create_csv_writer()

    csv_writer.write_row(["", "Total", "Data", "No Data", "Majority", "p", "l", "k"])
    current_row = []

    while text_file_reader.continue_reading:
        text_line = text_file_reader.read_line()
        text_line_split = text_line.split(" ")
        if " c " in text_line:
            filename = text_line_split[3]
            print filename
            csv_writer.write_row([filename])
        elif "ccode column_index " in text_line:
            column_index = text_line_split[2]
            if column_index != "0":
                current_row = ["column " + column_index]
        elif "!no_data_majority" in text_line:
            current_row.append("DATA")
        elif "no_data_majority" in text_line:
            current_row.append("NO_DATA")
        elif ("p = " in text_line) or ("l = " in text_line) or ("k = " in text_line) or ("a = " in text_line):
            val = text_line_split[2]
            val = "{0,1}" if val == "{0," else val
            current_row.append(val)
            if len(current_row) == 8 or val == "{0,1}":
                csv_writer.write_row(current_row)

    text_file_reader.close()
    csv_writer.close()

script()
