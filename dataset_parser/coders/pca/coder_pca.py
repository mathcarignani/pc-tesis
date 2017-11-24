from .. import coder_base


class CoderPCA(coder_base.CoderBase):
    def __init__(self, *args, **kwargs):
        super(CoderPCA, self).__init__(*args, **kwargs)
        # inputs
        self.ERROR_THRESHOLD = 10
        self.WINDOW_SIZE = 10
        # variables
        self._clear_window()

    def _clear_window(self):
        self.window = []
        self.window_min = None
        self.window_max = None
        self.window_constant = None

    def _code(self, value):
        value = self._map_value(value)
        if self._condition_holds(value):
            self.window.append(value)
            if len(self.window) == self.WINDOW_SIZE:
                self._code_window_constant()
                self._clear_window()
        else:
            self._code_window_incomplete()
            self._clear_window()
            self._condition_holds(value)
            self.window.append(value)

    def _map_value(self, value):
        if value == self.NO_DATA:
            return None
        value = float(value) * 1000000
        value = int(value)
        return value

    def _code_window_constant(self):
        self.output_file.write_bit(0)  # fi = 0
        self._code_raw(self.window_constant)

    def _code_window_incomplete(self):
        for value in self.window:
            self.output_file.write_bit(1)  # fi = 1
            self._code_raw(value)

    def _code_raw(self, value):
        if value is None:
            self.output_file.write_bit(1)  # nodata = 1
        else:
            self.output_file.write_bit(0)  # nodata = 0
            self.output_file.write_int(value, 24)

    def _condition_holds(self, value):
        if value is None:
            return self.window_constant is None
        else:
            if not self.window:  # empty window
                self.window_min = value
                self.window_max = value
                self.window_constant = 0
                return True
            elif value < self.window_min:
                self.window_min = value
                self.window_constant = (self.window_max - self.window_min) / 2
                return self.window_constant < self.ERROR_THRESHOLD
            elif value > self.window_max:
                self.window_max = value
                self.window_constant = (self.window_max - self.window_min) / 2
                return self.window_constant < self.ERROR_THRESHOLD
            return True
