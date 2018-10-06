import sys
sys.path.append('.')

from auxi.os_utils import python_project_path
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

mask_true_path = python_project_path() + "/scripts/compress/output/pwlh-vs-pwlhint-mask-true"
mask_false_path = python_project_path() + "/scripts/compress/output/pwlh-vs-pwlhint-mask-false"
path = mask_true_path

pwlh_filename = "results-pwlh.csv"
pwlh_int_filename = "results-pwlh-int.csv"
results_filename = "pwlh_vs_pwhl_int.csv"

csv_reader_pwlh = CSVReader(path, pwlh_filename)
csv_reader_pwlh_int = CSVReader(path, pwlh_int_filename)
csv_writer_results = CSVWriter(path, results_filename)

assert(csv_reader_pwlh.total_lines == csv_reader_pwlh_int.total_lines)


def compare_lines(a, b, c):
    return compare_lines_(a, b, c)


def run():
    while csv_reader_pwlh.continue_reading:
        assert(csv_reader_pwlh.current_line_count == csv_reader_pwlh_int.current_line_count)
        current_line_count = csv_reader_pwlh.current_line_count

        line_pwlh = csv_reader_pwlh.read_line()
        line_pwlh_int = csv_reader_pwlh_int.read_line()

        line = compare_lines(line_pwlh, line_pwlh_int, current_line_count)
        csv_writer_results.write_row(line)

    csv_reader_pwlh.close()
    csv_reader_pwlh_int.close()
    csv_writer_results.close()


def compare_lines_(line_pwlh, line_pwlh_int, line_count):
    assert(len(line_pwlh) == len(line_pwlh_int))

    # ['Dataset', 'Filename', '#rows', 'Coder', '%', 'Error Threshold', 'Window Param', 'Size (B)', 'CR (%)',
    #  'Delta - Size (data)', 'Delta - Size (mask)', 'Delta - Size (total)', 'Delta - CR (%)',
    #  'Other columns - Size (data)', 'Other columns - Size (mask)', 'Other columns - Size (total)', 'Other columns - CR (%)']
    if line_count == 0:
        assert(line_pwlh == line_pwlh_int)
        del line_pwlh[3]
        line = line_pwlh[:6] + line_pwlh[12:]
        line = line[:7]
        # ['Dataset', 'Filename', '#rows', '%', 'Error Threshold', 'Window Param', 'Other columns - Size (data)']
        return line

    # leave first 7 entries unchanged
    line = line_pwlh[:7]

    # ['IRKIS', 'vwc_1202.dat.csv', '26.305', 'CoderBasic', '', '', '']
    if line[3] == "CoderBasic":
        assert(line_pwlh == line_pwlh_int)
        del line[3]
        # ['IRKIS', 'vwc_1202.dat.csv', '26.305', '', '', '']
        return line

    if line[3] == "CoderPWLH":
        assert(line_pwlh[:3] == line_pwlh_int[:3])
        assert(line_pwlh[3] == "CoderPWLH" and line_pwlh_int[3] == "CoderPWLHint")
        assert(line_pwlh[4:7] == line_pwlh_int[4:7])
    else:
        assert(line_pwlh[:7] == line_pwlh_int[:7])

    # ['Delta - Size (data)', 'Delta - Size (mask)', 'Delta - Size (total)', 'Delta - CR (%)',
    #  'Other columns - Size (data)', 'Other columns - Size (mask)', 'Other columns - Size (total)', 'Other columns - CR (%)']
    values_line_pwlh = line_pwlh[9:]
    values_line_pwlh_int = line_pwlh_int[9:]

    values_line = []
    for i, value_pwlh in enumerate(values_line_pwlh):
        value_pwlh_int = values_line_pwlh_int[i]
        if value_pwlh == value_pwlh_int:
            values_line.append("0")
            continue

        if "." in value_pwlh:
            values_line.append("")
            continue

        assert(value_pwlh == str(int(value_pwlh)))
        assert(value_pwlh_int == str(int(value_pwlh_int)))

        value_pwlh = int(value_pwlh)
        value_pwlh_int = int(value_pwlh_int)
        assert(value_pwlh > 0)
        assert(value_pwlh_int > 0)
        diff = value_pwlh - value_pwlh_int
        if diff == 0:
            values_line.append("=====")
            continue

        if diff > 0:  # value_pwlh > value_pwlh_int
            best_str = "INT "
            big = value_pwlh
            small = value_pwlh_int
        else:  # value_pwlh < value_pwlh_int
            best_str = "FLT "
            big = value_pwlh_int
            small = value_pwlh

        val = (float(small) / float(big)) * 100
        val = best_str + "%0.2f" % val + "%"
        values_line.append(val)

    # ['Delta - Size (data)', 'Delta - Size (mask)', 'Delta - Size (total)', 'Delta - CR (%)']
    assert(values_line[:4] == ["0", "0", "0", "0"])

    # ['Other columns - Size (data)', 'Other columns - Size (mask)', 'Other columns - Size (total)', 'Other columns - CR (%)']
    values_line = values_line[4:]
    filtered_values_line = []
    for i, value in enumerate(values_line):
        if i % 4 == 0:
            # 'Other columns - Size (data)'
            filtered_values_line.append(value)

    del line[3]
    line = line + filtered_values_line
    return line

run()
