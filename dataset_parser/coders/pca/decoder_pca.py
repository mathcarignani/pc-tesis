from .. import decoder_base
from pca import PCA


class DecoderPCA(decoder_base.DecoderBase, PCA):
    def __init__(self, *args, **kwargs):
        PCA.__init__(self)
        super(DecoderPCA, self).__init__(*args, **kwargs)
        self._new_window(0, None)

    def _decode(self):
        if self.window['count'] > 0:
            return self._window_value()
        else:
            fi = self.input_file.read_bit()
            if fi == 0:
                print 'fi==0'
                print self.window
                self._new_window(self.WINDOW_SIZE, self._decode_value())
                a = self._window_value()
                print a
                return a

            else:  # fi == 1
                print 'fi==1'
                return self._decode_raw()

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

    def _decode_raw(self):
        return self.input_file.read_int(24)
