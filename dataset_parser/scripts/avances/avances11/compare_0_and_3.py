import sys
sys.path.append('.')

# from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.math_utils import MathUtils
from scripts.compress.experiments_utils import ExperimentsUtils

path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-11/3-results"


def get_coder_params(line):
    return line[:7]


def get_before_delta(line):
    return line[:9]


def get_delta_data(line):
    return line[9:13]


def get_after_delta(line):
    return line[13:]


def remove_delta_data(line):
    return get_before_delta(line) + get_after_delta(line)

########################################################################################################################


def print_percentage_diff(value0, value3):
    value0float, value3float = float(value0), float(value3)
    if value0float > value3float:
        if value3float == 0:
            return "AC"
        else:
            return str(MathUtils.calculate_percent(value0float, value3float)) + " % AC"
    elif value3float > value0float:
        if value0float == 0:
            return "NM"
        else:
            return str(MathUtils.calculate_percent(value3float, value0float)) + " % NM"
    else:  # equal
        return "="


def process_line(line0, line3, count):
    if count == 0:
        assert(line0 == line3)
        new_line = get_coder_params(line0)
        new_line += ["Size (B) Diff", "Size (B) Diff %",
                     "Other columns - Size (data)", "Other columns - Size (data) %",
                     "Other columns - Size (mask)", "Other columns - Size (mask) %",
                     "Other columns - Size (total)", "Other columns - Size (total) %"]
        return new_line

    new_line = get_coder_params(line0)

    # Size (B) | CR (%)
    size_bytes_0, size_bytes_3 = MathUtils.str_to_int(line0[7]), MathUtils.str_to_int(line3[7])
    new_line.append(MathUtils.print_absolute_diff(size_bytes_0, size_bytes_3))
    new_line.append(print_percentage_diff(size_bytes_0, size_bytes_3))

    after_delta0, after_delta3 = get_after_delta(line0), get_after_delta(line3)
    current_index = 0
    finished = False
    # Other columns - Size (data) | Other columns - Size (mask) | Other columns - Size (total) | Other columns - CR (%)
    while not finished:
        if current_index >= len(after_delta0) or after_delta0[current_index] is None:
            finished = True
            continue
        for i in [0, 1, 2]:
            value0, value3 = MathUtils.str_to_int(after_delta0[current_index + i]), MathUtils.str_to_int(after_delta3[current_index + i])
            new_line.append(MathUtils.print_absolute_diff(value0, value3))
            new_line.append(print_percentage_diff(value0, value3))
        current_index += 4
    return new_line


def run():
    csv_reader0 = CSVReader(path + "/MASK_MODE_0-results-ubuntu", "results-0-ubuntu.csv")
    csv_reader3 = CSVReader(path + "/MASK_MODE_3-results-ubuntu", "results-3-ubuntu.csv")
    csv_writer = CSVWriter(path, "0vs3.csv")

    coder = None
    count = 0
    while csv_reader0.continue_reading:
        line3 = csv_reader3.read_line()
        coder = line3[3] or coder
        if coder in ExperimentsUtils.CODERS_ONLY_MASK_MODE:
            continue
        line0 = csv_reader0.read_line()
        new_line = process_line(line0, line3, count)
        if new_line is not None:
            csv_writer.write_row(new_line)
        count += 1

    csv_reader0.close()
    csv_reader3.close()
    csv_writer.close()

# run()

########################################################################################################################


def best_values():
    csv_reader = CSVReader(path, "0vs3.csv")

    smallest_AC = 100
    smallest_NM = 100
    count = 0
    while csv_reader.continue_reading:
        line = csv_reader.read_line()
        if count == 0:
            count += 1
            continue
        if line[3] == "CoderBase":
            count += 1
            continue
        percentage = line[8]
        value = float(percentage.replace(" % AC", "").replace(" % NM", ""))
        if " % AC" in percentage:
            if value < smallest_AC:
                smallest_AC = value
                print("AC - " + str(count))
        elif " % NM" in percentage:
            if value < smallest_NM:
                smallest_NM = value
                print("NM - " + str(count))
        else:
            raise("ERROR")
        count += 1
    csv_reader.close()

    print("smallest_AC = " + str(smallest_AC))
    print("smallest_NM = " + str(smallest_NM))

# best_values()
