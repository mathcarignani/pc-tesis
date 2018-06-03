import sys
sys.path.append('.')


class WindowCA(object):
    def __init__(self, params):
        self.nan = "N"  # This is the value that represents nodata
        self.error_threshold = params['error_threshold']
        self.max_window_size = params['max_window_size']
        self.create_nan_window()
        self.current_window_length = 0

    def create_non_nan_window(self, incoming_value):
        self.archived_value = Point(0, incoming_value)
        self.snapshot_value = self.archived_value
        self.current_window_length = 0
        self.s_min = None  # Line
        self.s_max = None  # Line

    def create_nan_window(self):
        self.archived_value = None  # we do not use this value
        self.snapshot_value = self.nan
        self.current_window_length = 1
        self.s_min = None  # we do not use this value
        self.s_max = None  # we do not use this value

    def is_full(self):
        return self.current_window_length == self.max_window_size

    def is_empty(self):
        return self.current_window_length == 0

    def code(self, incoming_value, coder):
        if incoming_value is None:
            # print "(1) incoming_value is None:"
            coder.code_window(self.current_window_length, self._snapshot_value())  # Force code window

        elif self.is_full():
            # print "(2) self.is_full():"
            coder.code_window(self.current_window_length, self._snapshot_value())
            if incoming_value == self.nan:
                self.create_nan_window()
            else:
                incoming_value = int(incoming_value)
                coder.code_window(1, incoming_value)  # code single value window
                self.create_non_nan_window(incoming_value)

        elif self.is_empty():
            # print "(3) self.is_empty():"
            if incoming_value == self.nan:  # This condition can only be true on the first iteration
                self.create_nan_window()
            else:
                incoming_value = int(incoming_value)
                if self.archived_value:
                    # print "(3.2)"
                    self.current_window_length = 1
                    self.snapshot_value = Point(self.current_window_length, incoming_value)
                    self.s_min = self.archived_value.s_min(self.snapshot_value, self.error_threshold)
                    self.s_max = self.archived_value.s_max(self.snapshot_value, self.error_threshold)
                else:
                    # print "(3.3)"
                    coder.code_window(1, incoming_value)  # code single value window
                    self.create_non_nan_window(incoming_value)

        elif incoming_value == self.nan:
            # print "(4) incoming_value == self.nan:"
            if self.snapshot_value == self.nan:
                self.current_window_length += 1
            else:
                coder.code_window(self.current_window_length, self._snapshot_value())
                self.create_nan_window()

        else:
            # print "(5) else:"
            incoming_value = int(incoming_value)
            if self.snapshot_value == self.nan:
                # print "(5.1)"
                coder.code_window(self.current_window_length, self._snapshot_value())  # code nan window
                coder.code_window(1, incoming_value)  # code single value window
                self.create_non_nan_window(incoming_value)
            else:
                incoming_point = Point(self.current_window_length + 1, incoming_value)
                # incoming_point._print()
                if self.s_min.point_below_line(incoming_point) or self.s_max.point_above_line(incoming_point):
                    # print "(5.2)"
                    # incoming_point._print()
                    coder.code_window(self.current_window_length, self._snapshot_value())
                    coder.code_window(1, incoming_value)  # code single value window
                    self.create_non_nan_window(incoming_value)
                else:
                    # print "(5.3)"
                    # incoming_point._print()
                    self.snapshot_value = incoming_point
                    self._update_s_min_and_s_max(incoming_point)
                    self.current_window_length += 1

    def _update_s_min_and_s_max(self, incoming_point):
        s_min_new = self.archived_value.s_min(incoming_point, self.error_threshold)
        s_max_new = self.archived_value.s_max(incoming_point, self.error_threshold)

        if s_min_new.y_intersection(incoming_point) > self.s_min.y_intersection(incoming_point):
            self.s_min = s_min_new

        if s_max_new.y_intersection(incoming_point) < self.s_max.y_intersection(incoming_point):
            self.s_max = s_max_new

    def _snapshot_value(self):
        if self.snapshot_value == self.nan:
            return self.nan
        else:
            return self.snapshot_value.y

    def print_state(self):
        if self.archived_value is None:
            print "archived_value = None"
        elif self.archived_value == self.nan:
            print "archived_value = self.nan"
        else:
            print "archived_value = " + self.archived_value.to_str()
        if self.snapshot_value is None:
            print "snapshot_value = None"
        elif self.snapshot_value == self.nan:
            print "snapshot_value = self.nan"
        else:
            print "snapshot_value = " + self.snapshot_value.to_str()
        if self.s_min is None:
            print "s_min = None"
        else:
            print "s_min = " + self.s_min.to_str()
        if self.s_max is None:
            print "s_max = None"
        else:
            print "s_max = " + self.s_max.to_str()


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def s_min(self, point, error_threshold):
        point_minus_threshold = Point(point.x, point.y - error_threshold)
        return Line(self.copy(), point_minus_threshold)

    def s_max(self, point, error_threshold):
        point_plus_threshold = Point(point.x, point.y + error_threshold)
        return Line(self.copy(), point_plus_threshold)

    def _print(self):
        print "x=%s, y=%s" % (self.x, self.y)

    # def to_str(self):
    #     return "(x,y)=(%s,%s)" % (self.x, self.y)


class Line(object):
    #
    # PRE: point2.x > point1.x
    #
    def __init__(self, point1, point2):
        self.point = point1  # always matches self.archived_value, so point1.x = 0
        self.m = 0 if point1.y == point2.y else float(point2.y - point1.y) / point2.x

    def point_below_line(self, point):
        return self._check_point(point) == -1

    def point_above_line(self, point):
        return self._check_point(point) == 1

    #
    # Returns the position of the point regarding the line.
    #
    def _check_point(self, point):
        y_inter = self.y_intersection(point)
        # print "y_inter=%s, point.y=%s" % (y_inter, point.y)
        if y_inter == point.y:
            return 0  # the point is inside the line
        elif y_inter > point.y:
            return -1  # the point is below the line
        else:  # y_inter < point.y
            return 1  # the point is above the line

    #
    # Returns the y coordinate of the intersection between self and the vertical line that passes through point.
    #
    def y_intersection(self, point):
        return self.m * point.x + self.point.y

    def to_str(self):
        return "(x,y,m)=(%s,%s,%s)" % (self.point.x, self.point.y, self.m)
