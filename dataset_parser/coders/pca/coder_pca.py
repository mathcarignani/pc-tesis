from .. import coder_base
from pca import PCA
from window import Window


class CoderPCA(coder_base.CoderBase, PCA):
    def __init__(self, *args, **kwargs):
        PCA.__init__(self)
        super(CoderPCA, self).__init__(*args, **kwargs)
        self.window = Window(self.WINDOW_SIZE, self.ERROR_THRESHOLD)

    def _code(self, value):
        value = None if value == self.NO_DATA else value
        if self.window.condition_holds(value):
            print 'holds', value
            if self.window.full():
                self._code_window_constant()
                self.window.clear()
        else:
            print 'noholds', value
            self._code_window_incomplete()
            self.window.clear()
            self.window.condition_holds(value)

    def _code_window_constant(self):
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

    def _code_raw(self, value):
        self.output_file.write_int(value, 24)
