from .. import coder_base
from pca import PCA


class CoderPCA(coder_base.CoderBase, PCA):
    def __init__(self, input_path, input_filename, output_path, output_filename, params):
        super(CoderPCA, self).__init__(input_path, input_filename, output_path, output_filename)
        PCA.__init__(self, params)

    def _code(self, value):
        value = self._map_value(value)
        if self.window.condition_holds(value):
            if self.window.full():
                self._code_window()
                self.window.clear()
        else:
            self._code_window_incomplete()
            self.window.clear()
            self.window.condition_holds(value)

    def _map_value(self, value):
        value = None if value == self.nodata else value
        return value

    def _code_window(self):
        self.output_file.write_bit(0)  # fi = 0
        self._code_value(self.window.constant())

    def _code_window_incomplete(self):
        for value in self.window.array:
            self.output_file.write_bit(1)  # fi = 1
            self._code_value(value)

    def _code_value(self, value):
        if value is None:
            self.output_file.write_bit(1)  # nodata = 1
        else:
            self.output_file.write_bit(0)  # nodata = 0
            self._code_raw(value)
