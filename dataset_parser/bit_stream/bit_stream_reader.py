from utils import Utils


class BitStreamReader(object):
    def __init__(self, path, filename):
        self.continue_reading = True
        self.file = open(path + "/" + filename, 'rb')
        self.current = self._read_byte()
        self.offset = 0

    # PRE: self.continue_reading
    def read_bit(self):
        ans = self.current & (1 << self.offset)
        self.offset = (self.offset + 1) & 7

        if self.offset == 0:
            self.current = self._read_byte()

        return 0 if ans == 0 else 1

    # k is the number of bits we want to read
    def read_int(self, k):
        ans = 0
        for i in xrange(k-1, -1, -1):
            if self.continue_reading:
                bit = self.read_bit()
                ans |= bit << i
            else:
                raise AssertionError('Reached EOF.')
        return ans

    def close(self):
        self.file.close()

    # PRE: self.continue_reading
    def _read_byte(self):
        byte = self.file.read(1)
        if byte != '':  # EOF
            return Utils.decode_byte(byte)
        else:
            self.continue_reading = False
            return None
