# TODO: remove
import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.csv_utils.csv_reader import CSVReader

import os
path = os.path.dirname(os.path.abspath(__file__))
filename = 'test.csv'


def write_csv(rows):
    csv_writer = CSVWriter(path, filename)
    for row in rows:
        csv_writer.write_row(row)
    csv_writer.close()


def read_csv(expected_rows):
    csv_reader = CSVReader(path, filename)
    it = 0
    while csv_reader.continue_reading:
        row = csv_reader.read_row()
        expected_row = expected_rows[it]
        if expected_row != row:
            print 'row', row, 'expected_row', expected_row
            raise AssertionError('ERROR.')
        it += 1
    csv_reader.close()


def test(rows):
    print '.',
    write_csv(rows)
    read_csv(rows)


test([['Column 1', 'Column 2', 'Column 3']])
test([['Column 1', 'Column 2', 'Column 3'], ['value 1', 'value 2', 'value 3']])
os.remove(path + "/" + filename)
print 'SUCCESS!'
