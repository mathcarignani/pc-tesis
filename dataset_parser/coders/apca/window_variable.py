class WindowVariable(object):
    def __init__(self, params):
        self.nan = "N"  # This is the value that represents nodata
        self.error_threshold = params['error_threshold']
        self.max_window_size = params['max_window_size']
        self.clear()

    def clear(self):
        self.current_window, self.current_window_length = [], 0
        self.min, self.max, self.constant = [self.nan] * 3

    def is_full(self):
        return self.current_window_length == self.max_window_size

    def is_empty(self):
        return self.current_window_length == 0

    #
    # PRE: not self.is_full()
    #
    def add_value_2_output(self, value):
        self.current_window.append(value)
        self.current_window_length += 1
        return True

    def condition_holds(self, value):
        if self.is_full():
            return False

        if value is self.nan:
            if self.constant == self.nan:
                return self.add_value_2_output(self.nan)
            else:
                return False

        value = int(value)

        if self.is_empty():
            self.min, self.max, self.constant = [value] * 3
            return self.add_value_2_output(value)

        if self.constant is self.nan:
            return False

        if value < self.min:
            return self._update_constant(value, value, self.max)
        elif value > self.max:
            return self._update_constant(value, self.min, value)
        else:  # self.min <= value <= self.max
            return self.add_value_2_output(value)

    def _update_constant(self, value, new_min, new_max):
        new_min_aux = new_min + abs(new_min)  # >= 0
        new_max_aux = new_max + abs(new_min)  # >= 0

        if new_max_aux - new_min_aux > 2*self.error_threshold:  # condition does not hold
            return False

        # condition holds, update min, max and constant
        self.min, self.max = new_min, new_max
        self.constant = self.min + self.max
        self.constant = self.constant / 2 if self.constant != 0 else 0
        return self.add_value_2_output(value)
