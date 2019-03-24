import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-11/2-mask123"

csv_reader = CSVReader(path, "mask123-numbers.csv")
csv_writer = CSVWriter(path, "mask123-numbers-relative.csv")


def relative_diff(big, small):
    val = (float(big) / float(small))  # * 100
    val = "%0.2f" % val  # + "%"
    return val


def read_values(line, x):
    return int_value(line, x), int_value(line, 7 + x), int_value(line, 14 + x)


def int_value(line, index):
    value = line[index]
    if len(value) == 0:
        return None
    value = value.replace(",", "")
    return int(value)


def process_values(value1, value2, value3):
    if value1 is None:
        return None, None, None

    if value1 <= value2 and value1 <= value3:
        smallest = value1
    elif value2 <= value1 and value2 <= value3:
        smallest = value2
    else:
        smallest = value3
    new_value1 = relative_diff(value1, smallest)
    new_value2 = relative_diff(value2, smallest)
    new_value3 = relative_diff(value3, smallest)
    return new_value1, new_value2, new_value3


def process_line(line, count):
    if count == 0:
        return line

    li = line[-21:]
    array1, array2, array3 = [], [], []
    for x in range(0, 7):  # 0..6
        value1, value2, value3 = read_values(li, x)
        value1, value2, value3 = process_values(value1, value2, value3)
        array1.append(value1), array2.append(value2), array3.append(value3)
    return line[:3] + array1 + array2 + array3


def run():
    count = 0
    while csv_reader.continue_reading:
        line = csv_reader.read_line()
        new_line = process_line(line, count)
        csv_writer.write_row(new_line)
        count += 1

    csv_reader.close()
    csv_writer.close()

run()
