from .. import coder_base
from pca import PCA


class CoderPCA(coder_base.CoderBase, PCA):
    def __init__(self, *args, **kwargs):
        PCA.__init__(self)
        super(CoderPCA, self).__init__(*args, **kwargs)
        self._clear_window()

    def _clear_window(self):
        self.window = {'array': [], 'min': None, 'max': None, 'constant': None}

    def _code(self, value):
        value = self._map_value(value)
        if self._condition_holds(value):
            self.window['array'].append(value)
            if self._full_window():
                self._code_window_constant()
                self._clear_window()
        else:
            self._code_window_incomplete()
            self._clear_window()
            self._condition_holds(value)
            self.window['array'].append(value)

    # TODO: this should not be part of the decoder...
    def _map_value(self, value):
        if value == self.NO_DATA:
            return None
        value = float(value) * 1000000
        value = int(value)
        return value

    def _full_window(self):
        len(self.window['array']) == self.WINDOW_SIZE

    def _code_window_constant(self):
        self.output_file.write_bit(0)  # fi = 0
        self._code_raw(self.window['min'] + self.window['constant'])

    def _code_window_incomplete(self):
        for value in self.window['array']:
            self.output_file.write_bit(1)  # fi = 1
            self._code_raw(value)

    def _code_raw(self, value):
        if value is None:
            self.output_file.write_bit(1)  # nodata = 1
        else:
            self.output_file.write_bit(0)  # nodata = 0
            self._code_value(value)

    def _code_value(self, value):
        self.output_file.write_int(value, 24)

    def _condition_holds(self, value):
        if value is None:
            return self.window['constant'] is None
        elif not self.window['array']:  # empty window
            self.window.update({'min': value, 'max': value, 'constant': 0})
            return True
        elif value < self.window['min']:
            self.window.update({'min': value})
            return self._update_constant()
        elif value > self.window['max']:
            self.window.update({'max': value})
            return self._update_constant()
        return True

    def _update_constant(self):
        self.window.update({'constant': (self.window['max'] - self.window['min']) / 2})
        return self.window['constant'] < self.ERROR_THRESHOLD
