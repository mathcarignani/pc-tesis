import sys
sys.path.append('.')

import coders.pca.window_utils as window_utils


class WindowVariable(object):
    def __init__(self, params):
        self.nan = "N"  # This is the value that represents nodata
        self.error_threshold = params['error_threshold']
        self.max_window_size = params['max_window_size']
        self.clear()

    def clear(self, value=None):
        self.current_window_length = 0
        self.min, self.max, self.constant = [self.nan] * 3
        if value is not None:
            self.condition_holds(value)

    def is_full(self):
        return self.current_window_length == self.max_window_size

    def is_empty(self):
        return self.current_window_length == 0

    def condition_holds(self, value):
        if self.is_full():
            return False

        if value is self.nan:
            if self.constant == self.nan:
                self.current_window_length += 1
                return True
            else:
                return False

        value = int(value)

        if self.is_empty():
            self.min, self.max, self.constant = [value] * 3
            self.current_window_length += 1
            return True

        if self.constant is self.nan:
            return False

        if value < self.min:
            return self._update_constant(value, value, self.max)
        elif value > self.max:
            return self._update_constant(value, self.min, value)
        else:  # self.min <= value <= self.max
            self.current_window_length += 1
            return True

    def _update_constant(self, value, new_min, new_max):
        if not window_utils.valid_threshold(new_min, new_max, self.error_threshold):  # condition does not hold
            return False

        # condition holds, update min, max and constant
        self.min, self.max = new_min, new_max
        self.constant = self.min + self.max
        self.constant = self.constant / 2 if self.constant != 0 else 0
        return self.add_value_2_output(value)
