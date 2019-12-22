from bit_stream_reader import BitStreamReader


class BitStreamUtils:
    @staticmethod
    def compare_files(path1, filename1, path2, filename2):
        bsr1 = BitStreamReader(path1, filename1)
        bsr2 = BitStreamReader(path2, filename2)
        byte1 = bsr1.current
        byte2 = bsr2.current
        byte_count = 1
        same_file = None
        while same_file is None:

            if byte1 is None:
                if byte2 is None:
                    print('SAME FILE!')
                    same_file = True
                else:
                    print('Reached EOF of file 1. DIFF at byte', byte_count)
                    same_file = False
                break
            elif byte2 is None:
                print('Reached EOF of file 2. DIFF at byte', byte_count)
                same_file = False
            else:
                # print "byte", byte_count, byte1, byte2
                if byte1 != byte2:
                    print('Difference at byte', byte_count)
                    same_file = False

            if same_file is None:
                byte1 = bsr1.read_byte()
                byte2 = bsr2.read_byte()
                byte_count += 1

        bsr1.close()
        bsr2.close()
        return same_file
