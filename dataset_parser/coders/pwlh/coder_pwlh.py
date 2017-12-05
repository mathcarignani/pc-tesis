from apca import APCA

import sys
sys.path.append('../')

from coders.apca.coder_apca import CoderAPCA


class CoderPWLH(CoderAPCA):
    def __init__(self, input_path, input_filename, output_path, output_filename, params):
        super(CoderPWLH, self).__init__(input_path, input_filename, output_path, output_filename, params)

    def _code_window(self):
        # code the first and last values of the line

        # self._code_value(self.window.constant())
        # code the timestamp of the last point
        self._code_timestamp()
