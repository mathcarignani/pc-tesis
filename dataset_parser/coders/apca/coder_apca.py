from apca import APCA

import sys
sys.path.append('../')

from coders.pca.coder_pca import CoderPCA


class CoderAPCA(CoderPCA, APCA):
    def __init__(self, *args, **kwargs):
        super(CoderPCA, self).__init__(*args, **kwargs)
        APCA.__init__(self)
        self.current_timestamp = 0

    def _code(self, value):
        value = self._map_value(value)
        if self.window.condition_holds(value):
            if self.window.full():
                self._code_window()
                self.window.clear()
        else:
            self._code_window()
            self.window.clear()
            self.window.condition_holds(value)
        self.current_timestamp += 1

    def _code_window(self):
        self._code_value(self.window.constant())
        self._code_timestamp()

    def _code_timestamp(self):
        self._code_raw(self.current_timestamp)
