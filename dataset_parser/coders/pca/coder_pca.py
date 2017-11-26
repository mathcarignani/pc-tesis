from .. import coder_base
from pca import PCA


class CoderPCA(coder_base.CoderBase, PCA):
    def __init__(self, *args, **kwargs):
        PCA.__init__(self)
        super(CoderPCA, self).__init__(*args, **kwargs)
        self.window = Window(self.WINDOW_SIZE, self.ERROR_THRESHOLD)

    def _code(self, value):
        value = self._map_value(value)
        if self.window.condition_holds(value):
            if self.window.full():
                self._code_window_constant()
                self.window.clear()
        else:
            self._code_window_incomplete()
            self.window.clear()
            self.window.condition_holds(value)

    # TODO: this should not be part of the decoder...
    def _map_value(self, value):
        if value == self.NO_DATA:
            return None
        value = float(value) * 1000000
        value = int(value)
        return value

    def _code_window_constant(self):
        self.output_file.write_bit(0)  # fi = 0
        self._code_raw(self.window.constant())

    def _code_window_incomplete(self):
        for value in self.window.array:
            self.output_file.write_bit(1)  # fi = 1
            self._code_raw(value)

    def _code_raw(self, value):
        if value is None:
            self.output_file.write_bit(1)  # nodata = 1
        else:
            self.output_file.write_bit(0)  # nodata = 0
            self.output_file.write_int(value, 24)


class Window(object):
    def __init__(self, window_size, error_threshold):
        self.window_size = window_size
        self.error_threshold = error_threshold
        self.clear()

    def clear(self):
        self.array, self.min, self.max, self.half = [], None, None, None

    def full(self):
        return len(self.array) == self.window_size

    def constant(self):
        return self.min + self.half

    def condition_holds(self, value):
        if value is None:
            if self.half is None:
                self.array.append(None)
                return True
            else:
                return False
        elif not self.array:
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