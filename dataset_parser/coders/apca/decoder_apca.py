import sys
sys.path.append('../')

from coders.pca.decoder_pca import DecoderPCA


class DecoderAPCA(DecoderPCA):
    def __init__(self, *args, **kwargs):
        super(DecoderAPCA, self).__init__(*args, **kwargs)
