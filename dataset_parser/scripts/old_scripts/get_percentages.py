import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter


def create_new_row(coder_basic_row, pwlh_row):
    initial = 8
    row_length = len(coder_basic_row)  # 13
    new_row = []

    for i in range(row_length):  # 1, 2, .., 12
        if i < initial or i % 2 != 0:
            new_row.append(pwlh_row[i])
        else:  # 8, 10, 12
            hundred_percent = float(coder_basic_row[i-1].replace('.', ''))
            unknown_percent = float(pwlh_row[i-1].replace('.', ''))
            val = round((100*unknown_percent)/hundred_percent, 3)
            new_row.append(val)
    return new_row


def parse_file(input_path, filename):
    csv_reader = CSVReader(input_path, filename)
    csv_writer = CSVWriter(input_path, filename + '-2.csv')

    processing_pwlh = False
    coder_basic_row = None

    while csv_reader.continue_reading:
        row = csv_reader.read_line()

        if row[3] == 'CoderBasic':
            processing_pwlh = False
            coder_basic_row = row
        elif row[3] == 'CoderPWLH':
            processing_pwlh = True

        if processing_pwlh is False:
            csv_writer.write_row(row)
        else:
            new_row = create_new_row(coder_basic_row, row)
            csv_writer.write_row(new_row)


input_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-dudas-4/results/MERGED_RESULTS"

filenames = ['results1_irkis.csv', 'results5_el-nino.csv', 'results2_noaa-sst.csv',
             'results6_noaa-spc-hail.csv', 'results3_noaa-adcp.csv',
             'results7_noaa-spc-tornado.csv', 'results4_solar-anywhere.csv',
             'results8_noaa-spc-wind.csv']

for filename in filenames:
    parse_file(input_path, filename)
