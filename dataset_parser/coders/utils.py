from coder_base import CoderBase
from decoder_base import DecoderBase
from pca.coder_pca import CoderPCA
from pca.decoder_pca import DecoderPCA
from apca.coder_apca import CoderAPCA
from apca.decoder_apca import DecoderAPCA
from file_utils.utils import Utils as FileUtils
from file_utils.scripts import Scripts as FileScripts



class Utils(object):
    # key: 'base', 'pca', 'apca'
    @staticmethod
    def code_decode(key, input_path, input_filename, output_path, coder_params={}):
        coded_filename = input_filename + '.' + key + '.code'
        decoded_filename = coded_filename + '.decode'

        coder, decoder = Utils.str_to_coder(key)

        print 'coding', key.upper(), '...', coder_params
        c = coder(input_path, input_filename, output_path, coded_filename, coder_params)
        c.code_file()
        c.close()

        coded_size = FileUtils.file_size(output_path, coded_filename)
        print 'size =', coded_size

        print 'decoding', key.upper(), '...'
        d = decoder(output_path, coded_filename, output_path, decoded_filename, coder_params)
        d.decode_file()
        d.close()

        print 'comparing original and decoded file...'
        FileScripts.compare_files(input_path, input_filename, decoded_filename, coder_params.get('error_threshold'))
        print

    @staticmethod
    def str_to_coder(key):
        return {
            'base': [CoderBase, DecoderBase],
            'pca': [CoderPCA, DecoderPCA],
            'apca': [CoderAPCA, DecoderAPCA]
        }[key]
