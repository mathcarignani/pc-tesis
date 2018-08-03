import sys
sys.path.append('.')

from file_utils.text_utils.text_file_reader import TextFileReader

# Comparing original and decompressed files...
# abs_diff 4 error_threshold 3
# row_count = 3197, col_index = 427, value1 = '2796', value2 = '2800'
# abs_diff 4 error_threshold 3
# row_count = 3201, col_index = 427, value1 = '2786', value2 = '2790'
# abs_diff 3 error_threshold 2
# row_count = 4488, col_index = 380, value1 = '16478', value2 = '16481'
# abs_diff 4 error_threshold 3
# row_count = 5008, col_index = 518, value1 = '2850', value2 = '2854'
# abs_diff 5 error_threshold 4
# row_count = 5120, col_index = 308, value1 = '2827', value2 = '2832'
# abs_diff 4 error_threshold 3
# row_count = 5620, col_index = 455, value1 = '2747', value2 = '2751'
#
# RESULTS
# ERROR: DIFFERENT FILES!
# CoderPWLHint
# ORIGINAL FILE:
# -> name: /Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[5]el-nino/el-nino.csv
# -> size (bytes): 9,820,158
# COMPRESSED FILE:
# -> name: /Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/[5]el-nino/pwlh-int/el-nino.c.cpp.csv
# -> size (bytes): 1,750,392
# -> 17.82% of original

path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output"
filename = "OUTPUT_FULL.txt"
expected_diff = 1

text_file = TextFileReader(path, filename)
while text_file.continue_reading:
    line = text_file.read_line()
    if "abs_diff" in line:
        line_array = line.split()
        abs_diff = int(line_array[1])
        error_threshold = int(line_array[3])
        assert(error_threshold != 0)
        diff = abs_diff - error_threshold
        if diff != expected_diff:
            print 'diff', diff
        assert(diff == expected_diff)

