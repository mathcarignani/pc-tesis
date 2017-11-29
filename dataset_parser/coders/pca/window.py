class Window(object):
    def __init__(self, window_size, error_threshold):
        self.window_size = window_size
        self.error_threshold = error_threshold
        self.clear()

    def clear(self):
        self.array, self.min, self.max, self.half = [], None, None, None

    def full(self):
        return len(self.array) == self.window_size

    def empty(self):
        return not self.array

    def constant(self):
        return None if self.half is None else self.min + self.half

    def condition_holds(self, value):
        if value is None:
            if self.half is None:
                self.array.append(None)
                return True
            else:
                return False
        elif self.empty:
            self.min, self.max, self.half = value, value, 0
            self.array.append(value)
            return True
        elif value < self.min:
            self.min = value
            return self._update_half(value)
        elif value > self.max:
            self.max = value
            return self._update_half(value)
        else:
            self.array.append(value)
            return True

    def _update_half(self, value):
        self.half = (self.max - self.min) / 2
        if self.half < self.error_threshold:
            self.array.append(value)
            return True
        else:
            return False

