import sys
sys.path.append('../')

from coders.pca.decoder_pca import DecoderPCA


class DecoderAPCA(DecoderPCA):
    def __init__(self, *args, **kwargs):
        super(DecoderPCA, self).__init__(*args, **kwargs)
        self.current_timestamp = 0
        self._new_window(0, None)

    def _decode(self):
        if self.window['count'] == 0:
            value = self._decode_value()
            last_timestamp = self._decode_timestamp()
            # if last_timestamp > 7823 and last_timestamp < 7830:
            #     print '\nlast_timestamp', last_timestamp
            self._new_window(last_timestamp - self.current_timestamp, value)
        self.current_timestamp += 1
        return self._window_value()

    def _decode_timestamp(self):
        return self._decode_raw()
