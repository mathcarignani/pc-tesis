
class CompressArgs:
    def __init__(self, args):
        self.logger = args['logger']
        self.coder = args['coder']
        self.coder_name = args['coder_name']
        self.coder_params = args['coder_params']
        self.decoder = args['decoder']
        self.input_path = args['input_path']
        self.input_filename = args['input_filename']
        self.output_path = args['output_path']

        self.compressed_filename = self.input_filename.replace('.csv', '.c.csv')
        self.deco_filename = self.input_filename.replace('.csv', '.c.d.csv')

        self.mask_mode = args['mask_mode']

    def code_cpp(self):
        self.compressed_filename = self.input_filename.replace('.csv', '.c.cpp.csv')

    def decode_cpp(self):
        self.deco_filename = self.input_filename.replace('.csv', '.c.d.cpp.csv')
