import sys
sys.path.append('../')

from coders.pca.coder_pca import CoderPCA


class CoderAPCA(CoderPCA):
    def __init__(self, *args, **kwargs):
        super(CoderAPCA, self).__init__(*args, **kwargs)
        self.current_timestamp = 0

    def _code(self, value):
        value = self._map_value(value)
        if not self.window.condition_holds(value):
            self._code_window_constant()
            self.window.clear()
            self.window.condition_holds(value)
        self.current_timestamp += 1

    def _code_window_constant(self):
        self._code_value(self.window.constant())
        self._code_timestamp()

    def _code_timestamp(self):
        self._code_raw(self.current_timestamp)