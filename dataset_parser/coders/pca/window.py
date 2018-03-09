class Window(object):
    #
    # There are three options for the window size parameters:
    # (1) If fixed_window_size == x and max_window_size is None => the window can have exactly x elements
    # (2) If fixed_window_size is None and max_window_size == x => the window can have up to x elements.
    # (3) If fixed_window_size is None and max_window_size is None => the window can have as much elements as possible.
    #
    def __init__(self, error_threshold, fixed_window_size, none, max_window_size=None):
        self.error_threshold = error_threshold
        self.fixed_window_size = fixed_window_size
        self.none = none
        self.max_window_size = max_window_size
        self.clear()

    def clear(self):
        self.array, self.min, self.max, self.half = [], self.none, self.none, self.none

    #
    # PRE: self.fixed_window_size and self.max_window_size cannot both be None.
    #
    def full(self):
        if self.fixed_window_size:
            return len(self.array) == self.fixed_window_size
        else:  # self.max_window_size
            return len(self.array) == self.max_window_size

    def empty(self):
        return not self.array

    def constant(self):
        if self.half is self.none:
            return self.none
        elif self.min == self.half:
            return self.min
        else:
            return self.min + self.half

    # def print_window(self):
    #     print 'min', self.min, 'max', self.max, 'half', self.half

    def condition_holds(self, value):
        if value is self.none:
            if self.half is self.none:
                self.array.append(self.none)
                return True
            else:
                return False
        elif self.empty():
            self.min, self.max, self.half = value, value, 0
            self.array.append(value)
            return True
        elif self.half is self.none:
            return False
        elif value < self.min:
            return self._update_half(value, value, self.max)
        elif value > self.max:
            return self._update_half(value, self.min, value)
        else:
            self.array.append(value)
            return True

    def _update_half(self, value, new_min, new_max):
        new_half = (new_max - new_min) / 2
        if new_half < self.error_threshold:
            self.min, self.max = new_min, new_max
            self.half = new_half
            self.array.append(value)
            return True
        else:
            return False

