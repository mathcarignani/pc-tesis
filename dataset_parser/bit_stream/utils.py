from bit_stream_reader import BitStreamReader


class Utils(object):
    @staticmethod
    def compare_files(path, filename1, filename2):
        bsr1 = BitStreamReader(path, filename1)
        bsr2 = BitStreamReader(path, filename2)
        byte_count = 0
        while True:
            byte_count += 1
            byte1 = bsr1.read_byte()
            byte2 = bsr2.read_byte()

            if byte1 is None:
                if byte2 is None:
                    print 'SAME FILE!'
                else:
                    print 'Reached EOF if file 1. DIFF at byte', byte_count
                break
            elif byte2 is None:
                print 'Reached EOF if file 2. DIFF at byte', byte_count
                break
        bsr1.close()
        bsr2.close()
