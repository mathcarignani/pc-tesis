from .. import decoder_base
from pca import PCA


class DecoderPCA(decoder_base.DecoderBase, PCA):
    def __init__(self, input_path, input_filename, output_path, output_filename, params):
        super(DecoderPCA, self).__init__(input_path, input_filename, output_path, output_filename)
        PCA.__init__(self, params)
        self._new_window(0, None)

    def _decode(self):
        if self.window['count'] > 0:
            return self._window_value()
        else:
            fi = self.input_file.read_bit()
            value = self._decode_value()
            if fi == 0:
                self._new_window(self.fixed_window_size, value)
                return self._window_value()

            else:  # fi == 1
                return value

    def _new_window(self, count, value):
        self.window = {'count': count, 'value': value}

    # PRE: self.window['count'] > 0
    def _window_value(self):
        self.window['count'] -= 1
        return self.window['value']

    def _decode_value(self):
        nodata = self.input_file.read_bit()
        if nodata == 1:
            return self.NO_DATA
        else:  # nodata == 0
            return self._decode_raw()
