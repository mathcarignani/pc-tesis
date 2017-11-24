from coder_base import CoderBase
from decoder_base import DecoderBase
from pca.coder_pca import CoderPCA
from pca.decoder_pca import DecoderPCA
from apca.coder_apca import CoderAPCA
from apca.decoder_apca import DecoderAPCA


class Utils(object):
    # key: 'base', 'pca', 'apca'
    @staticmethod
    def code_decode(key, input_path, input_filename, output_path):
        coded_filename = input_filename + '.' + key + '.code'
        decoded_filename = coded_filename + '.decode'

        coder, decoder = Utils.str_to_coder(key)

        c = coder(input_path, input_filename, output_path, coded_filename)
        c.code_file()
        c.close()

        d = DecoderBase(output_path, coded_filename, output_path, decoded_filename)
        d.decode_file()
        d.close()

    @staticmethod
    def str_to_coder(key):
        return {
            'base': [CoderBase, DecoderBase],
            'pca': [CoderPCA, DecoderPCA],
            'apca': [CoderAPCA, DecoderAPCA]
        }[key]
