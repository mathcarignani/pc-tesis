from file_reader import FileReader


class Scripts(object):
    @staticmethod
    def compare_files(path, filename1, filename2, error_threshold=15, nodata=None):
        NO_DATA = nodata if nodata is not None else 'nodata'
        fr1 = FileReader(path, filename1)
        fr2 = FileReader(path, filename2)
        line_count = 0
        while True:
            line_count += 1

            if not fr1.continue_reading:
                if not fr2.continue_reading:
                    print 'SAME FILE!'
                else:
                    print 'Reached EOF of file 1. DIFF at line', line_count
                break
            elif not fr2.continue_reading:
                print 'Reached EOF of file 2. DIFF at line', line_count
                break

            line1 = fr1.read_line()
            line2 = fr2.read_line()

            value1 = line1.rstrip('\n')
            value2 = line2.rstrip('\n')

            error = False
            if value1 == NO_DATA:
                if value2 != NO_DATA:
                    error = True
            elif value2 == NO_DATA:
                error = True
            else:
                diff = abs(int(value1) - int(value2))
                if diff > error_threshold:
                    error = True
            if error:
                print 'DIFF: value1=', value1, 'value2=', value2, 'line=', line_count
                break
        fr1.close()
        fr2.close()
