from text_file_reader import TextFileReader


class Utils(object):
    @staticmethod
    def compare_files(path, filename1, filename2, error_threshold=0, nodata='nodata'):
        error_threshold = 0 if error_threshold is None else error_threshold
        fr1 = TextFileReader(path, filename1)
        fr2 = TextFileReader(path, filename2)
        line_count = 0
        while True:
            line_count += 1

            if not fr1.continue_reading:
                if not fr2.continue_reading:
                    print('SAME FILE!')
                else:
                    print('Reached EOF of file 1. DIFF at line', line_count)
                break
            elif not fr2.continue_reading:
                print('Reached EOF of file 2. DIFF at line', line_count)
                break

            line1 = fr1.read_line()
            line2 = fr2.read_line()

            value1 = line1.rstrip('\n')
            value2 = line2.rstrip('\n')

            error = False
            if value1 == nodata:
                if value2 != nodata:
                    error = True
            elif value2 == nodata:
                error = True
            else:
                diff = abs(int(value1) - int(value2))
                # print 'diff', diff
                # print 'error_threshold', error_threshold
                if diff > error_threshold:
                    error = True
            if error:
                print('DIFF: value1=', value1, 'value2=', value2, 'line=', line_count)
                break
        fr1.close()
        fr2.close()

    @staticmethod
    def parse_file(path, filename, parser):
        fr = TextFileReader(path, filename, True)
        while fr.continue_reading:
            line = fr.read_line()
            parser.parse_line(line)
            # if fr.current_line_count == 1000:
            #     break
        fr.close()
