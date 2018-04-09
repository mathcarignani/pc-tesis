import sys
sys.path.append('../')

from coders.cols.decoder_cols import DecoderCols
from coders.ca.window_ca import Point, Line


class DecoderCA(DecoderCols):
    def __init__(self, input_path, input_filename, output_csv, params):
        super(DecoderCA, self).__init__(input_path, input_filename, output_csv)
        self.window_size_bit_length = params['max_window_size'].bit_length()

    def _decode_column(self):
        self.row_index, self.column = 0, []
        previous_value = None

        while self.row_index < self.data_rows_count:
            window_length, value = self._decode_window()
            if value == 'N' or previous_value == value or window_length == 1:
                window = [value] * window_length
            else:
                window = self._create_window(previous_value, value, window_length)
            previous_value = value
            self.column.extend(window)
            self.row_index += window_length

        return self.column

    def _decode_window(self, _=None):
        window_length = self.input_file.read_int(self.window_size_bit_length)
        value = self._decode_value_raw(self.row_index, self.column_index)
        return [window_length, value]

    #
    # PRE: window_length >= 2
    #
    @classmethod
    def _create_window(cls, previous_value, value, window_length):
        first_point = Point(0, previous_value)
        last_point = Point(window_length, value)
        line = Line(first_point, last_point)

        window = []
        for x in range(window_length):
            point = Point(x + 1, 0)  # y doesn't matter
            y = line.y_intersection(point)
            window.append(int(round(y)))

        if window[-1] != value:
            # print "first point:", 0, previous_value
            # print "last point:", window_length, value
            # print window
            # point = Point(7, 0)
            # print "line.point.x", line.point.x
            # print "line.point.y", line.point.y
            # print "line.m", line.m
            # y = line.y_intersection(point)
            # print "y", y
            # print "int(round(y))", int(round(y))
            raise StandardError("These two values must match. window[-1]=%s, value=%s" % (window[-1], value))

        return window
