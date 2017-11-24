from .. import decoder_base


class DecoderPCA(decoder_base.DecoderBase):
    def __init__(self, *args, **kwargs):
        super(DecoderPCA, self).__init__(*args, **kwargs)
