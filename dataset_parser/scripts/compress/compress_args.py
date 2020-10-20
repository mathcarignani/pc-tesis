
class CompressArgs:
    def __init__(self, compress_script, coder_params={}):
        self.logger = compress_script.logger
        self.coder = compress_script.coder_dictionary.get('coder')
        self.coder_name = compress_script.coder_dictionary['name']
        self.coder_params = coder_params
        self.decoder = compress_script.coder_dictionary.get('decoder')
        self.input_path = compress_script.input_path
        self.input_filename = compress_script.input_filename
        self.output_path = compress_script.output_dataset_coder_path
        self.mask_mode = compress_script.mask_mode

        self.compressed_filename = self.input_filename.replace('.csv', '.c.csv')
        self.deco_filename = self.input_filename.replace('.csv', '.c.d.csv')

    def code_cpp(self):
        self.compressed_filename = self.input_filename.replace('.csv', '.c.cpp.csv')

    def decode_cpp(self):
        self.deco_filename = self.input_filename.replace('.csv', '.c.d.cpp.csv')
