import sys
sys.path.append('.')

from file_utils.text_utils.text_file_reader import TextFileReader


def el_nino(name):
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[5]el-nino"
    input_filename = "el-nino.log"

    file_reader = TextFileReader(input_path, input_filename)

    min_line = 9
    max_line = 11
    name_line = 12
    diff = 8

    read_line = 1
    buoy_count = 0
    # buoy_total = 78

    min_min, max_max = None, None
    min_min_buoy, max_max_buoy = None, None
    mini, maxi = None, None

    while read_line < 4310 and file_reader.continue_reading:
        line = file_reader.read_line()
        is_min_line = (read_line >= min_line) and (read_line - min_line) % diff == 0
        is_max_line = (read_line >= min_line) and (read_line - max_line) % diff == 0
        is_name_line = (read_line >= min_line) and (read_line - name_line) % diff == 0

        if is_min_line or is_max_line:
            split = line.split(" ")
            str = 'min' if is_min_line else 'max'
            if split[0] != str:
                raise StandardError("ERROR %s != %s" % (split[0], str))
            value = float(split[-1])

            if is_min_line:
                mini = value
            else:  # is_max_line
                maxi = value

        elif is_name_line:
            if name in line:
                buoy_count += 1
                # print 'read_line', read_line
                # print 'line', line
                # print buoy_count
                if min_min is None or mini < min_min:
                    min_min = mini
                    min_min_buoy = buoy_count
                    # print 'min_min', read_line, min_min
                if max_max is None or maxi > max_max:
                    max_max = maxi
                    max_max_buoy = buoy_count
                    # print 'max_max', read_line, max_max

                mini, maxi = None, None
            else:
                mini, maxi = None, None

        read_line += 1

    print name
    print 'min', min_min, '=> buoy', min_min_buoy
    print 'max', max_max, '=> buoy', max_max_buoy
    print

for name in ['_lat', '_long', '_ZonWinds', '_MerWinds', '_Humidity', '_AirTemp', '_SST']:
    el_nino(name)
