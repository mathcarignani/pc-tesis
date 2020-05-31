import sys
sys.path.append('.')

import os
from datetime import datetime

from auxi.logger import setup_logger
from auxi.print_utils import PrintUtils
from auxi.os_utils import OSUtils
from file_utils.csv_utils.csv_compare import CSVCompare
from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.csv_utils.csv_utils import CSVUtils
from scripts.utils import create_folder
from scripts.compress.compress_utils import CompressUtils
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.compress.compress_cpp import CompressCPP
from scripts.compress.compress_args import CompressArgs


class CompressScript:
    COMPRESS_PATH = OSUtils.git_path() + "/dataset_parser/scripts/compress"
    OUTPUT_PATH = COMPRESS_PATH + "/output/"
    DATASETS_PATH = ExperimentsUtils.CSV_PATH

    def __init__(self, output_filename):
        self.csv = CSVWriter(self.OUTPUT_PATH, output_filename)

        # iteration vars
        self.logger = None
        self.output_dataset_path = None
        self.row = None
        self.thresholds_array = None
        self.input_path = None
        self.input_filename = None
        self.coder_dictionary = None
        self.output_dataset_coder_path = None


    def run(self):
        row = ['Dataset', 'Filename', '#rows', 'Coder', '%', 'Error Threshold', 'Window Param', 'Size (B)', 'CR (%)',
               'Delta - Size (data)', 'Delta - Size (mask)', 'Delta - Size (total)', 'Delta - CR (%)',
               'Other columns - Size (data)', 'Other columns - Size (mask)', 'Other columns - Size (total)', 'Other columns - CR (%)']
        self.csv.write_row(row)

        for dataset_dictionary in ExperimentsUtils.DATASETS_ARRAY:
            self._run_script_on_dataset(dataset_dictionary)
        self.csv.close()


    def _run_script_on_dataset(self, dataset_dictionary):
        self.input_path = self.DATASETS_PATH + dataset_dictionary['folder']
        logger_name = dataset_dictionary['name'].lower() + '.log'
        logger_filename = self.OUTPUT_PATH + logger_name
        self.logger = setup_logger(logger_name, logger_filename)

        self.output_dataset_path = self.OUTPUT_PATH + dataset_dictionary['o_folder']
        create_folder(self.output_dataset_path)
        dataset_name = dataset_dictionary['name']

        for file_index, self.input_filename in enumerate(ExperimentsUtils.dataset_csv_filenames(dataset_name)):
            self.row = [dataset_name] if file_index == 0 else [None]
            self._run_script_on_file(file_index)


    def _run_script_on_file(self, file_index):
        print(self.input_path + "/" + self.input_filename)
        base_values = None
        row_count = PrintUtils.separate(CSVUtils.csv_row_count(self.input_path, self.input_filename))

        # calculate error thresholds
        compress_utils = CompressUtils(self.COMPRESS_PATH, self.input_path, self.input_filename)
        self.thresholds_array = compress_utils.get_thresholds_array()

        for coder_index, self.coder_dictionary in enumerate(ExperimentsUtils.CODERS_ARRAY):
            # TODO: uncomment in ubuntu
            # if self.input_filename == "el-nino.csv" and self.coder_dictionary['name'] == "CoderGAMPS":
            #     continue
            # TODO: uncomment in mac
            if self.input_filename != "el-nino.csv" or self.coder_dictionary['name'] not in ["CoderBase", "CoderGAMPS"]:
                continue
                
            if file_index == 0 and coder_index == 0:  # first row of dataset and file
                self.row += [self.input_filename, row_count]
            elif coder_index == 0:  # first row of file
                self.row = [None, self.input_filename, row_count]
            else:
                self.row = [None, None, None]
            base_values = self._run_script_on_coder(base_values)


    def _run_script_on_coder(self, base_values):
        self.output_dataset_coder_path = self.output_dataset_path + '/' + self.coder_dictionary['o_folder']
        create_folder(self.output_dataset_coder_path)

        coder_name = self.coder_dictionary['name']
        if coder_name == 'CoderBase':
            base_values = self._run_script_on_base_coder(base_values)
        else:
            self._run_script_of_other_coders(base_values)
        return base_values


    def _run_script_on_base_coder(self, base_values):
        values = [self.coder_dictionary['name']] + [None] * 3
        compress_args = CompressArgs(self._compress_args())
        compression_values = CompressScript._compress_file(compress_args)
        base_values = self._out_results(base_values, compression_values, self.row + values)
        return base_values


    def _run_script_of_other_coders(self, base_values):
        window_param_name = list(self.coder_dictionary['params'].keys())[0]  # there's a single key
        window_sizes = self.coder_dictionary['params'][window_param_name]

        for thre_index, threshold_entry in enumerate(self.thresholds_array):
            percentage = threshold_entry['percentage']
            error_thresold_array = threshold_entry['values']
            params = {'error_threshold': error_thresold_array}
            for win_index, window_size in enumerate(window_sizes):
                values = [self.coder_dictionary['name']] if thre_index == 0 and win_index == 0 else [None]
                values += [percentage, params['error_threshold']] if win_index == 0 else [None, None]
                values += [window_size]

                params[window_param_name] = window_size
                compress_args = CompressArgs(self._compress_args(params))
                compression_values = CompressScript._compress_file(compress_args)
                base_values = self._out_results(base_values, compression_values, self.row + values)
        return base_values


    def _compress_args(self, coder_params={}):
        args = {
            'logger': self.logger,
            'coder': self.coder_dictionary.get('coder'),
            'coder_name': self.coder_dictionary['name'],
            'coder_params': coder_params,
            'decoder': self.coder_dictionary.get('decoder'),
            'input_path': self.input_path,
            'input_filename': self.input_filename,
            'output_path': self.output_dataset_coder_path
        }
        return args


    @staticmethod
    def _compress_decompress_compare(args):
        print("Compressing and decompressing files...")
        coder_info, header_bits, columns_bits, column_mask_bits = CompressCPP.code_decode_cpp(args)
        print("Comparing original and decompressed files...")
        csv_compare = CSVCompare(args.input_path, args.input_filename, args.output_path, args.deco_filename)
        # TODO: the csv comparison would be faster if implemented in C++
        same_file = csv_compare.compare(args.coder_params.get('error_threshold'), False)
        if not same_file:
            print("ERROR / ERROR / ERROR: DIFFERENT FILES!")
        assert same_file

        return [coder_info, header_bits, columns_bits, column_mask_bits, same_file]


    @staticmethod
    def _compress_file(args):
        coder_info, header_bits, columns_bits, column_mask_bits, same_file = CompressScript._compress_decompress_compare(args)

        # print results
        input_file = args.input_path + "/" + args.input_filename
        compressed_file = args.output_path + "/" + args.compressed_filename
        compressed_size = CompressScript._print_results(coder_info, args.logger, input_file, compressed_file, same_file)
        CompressScript._size_check(compressed_size, header_bits, columns_bits, column_mask_bits)
        compression_values = []
        for i in range(0, len(columns_bits)):
            compression_values.append(columns_bits[i])
            compression_values.append(column_mask_bits[i])
            compression_values.append(columns_bits[i] + column_mask_bits[i])
        return [compressed_size] + compression_values


    @staticmethod
    def _print_results(coder_info, logger, input_file, compressed_file, same_file):
        input_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(compressed_file)
        logger.info("")
        logger.info("RESULTS")
        if same_file:
            logger.info("--------------------------(same file!)")
        else:
            logger.info("ERROR: DIFFERENT FILES!")
            # raise StandardError("ERROR: DIFFERENT FILES!")
        logger.info(coder_info)
        logger.info("TIME: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logger.info("ORIGINAL FILE:")
        logger.info("-> name: %s" % input_file)
        logger.info("-> size (bytes): %s" % "{:,}".format(input_size))
        logger.info("COMPRESSED FILE:")
        logger.info("-> name: %s" % compressed_file)
        logger.info("-> size (bytes): %s" % "{:,}".format(compressed_size))
        logger.info("-> %s%% of original" % PrintUtils.percentage(compressed_size, input_size))
        logger.info("")
        return compressed_size


    @staticmethod
    def _size_check(compressed_size, header_bits, columns_bits, column_mask_bits):
        bits_sum = header_bits + sum(columns_bits) + sum(column_mask_bits)
        bytes_sum = (bits_sum + 7) // 8
        if compressed_size != bytes_sum:
            print("compressed_size " + str(compressed_size))
            print("bytes_sum " + str(bytes_sum))
        assert(compressed_size == bytes_sum)

        header_bytes = (header_bits + 7) // 8
        max_header_size = 15000
        if header_bytes >= max_header_size:
            print('header_bytes = %s' % header_bytes)
        assert(header_bytes < max_header_size)


    def _out_results(self, base_values, compression_values, row):
        values = []
        if base_values is None:
            base_values = compression_values
            for idx, value in enumerate(compression_values):
                if (idx % 3) == 0:  # idx is 0, 3, 6, 9, 12, etc.
                    val = PrintUtils.separate(value) if idx == 0 else value
                    values += [val, 100]
                else:
                    values += [value]
        else:
            for idx, value in enumerate(compression_values):
                if (idx % 3) == 0:  # idx is 0, 3, 6, 9, 12, etc.
                    percentage = PrintUtils.percentage(value, base_values[idx])
                    val = PrintUtils.separate(value) if idx == 0 else value
                    values += [val, PrintUtils.separate(percentage)]
                else:
                    values += [value]
        self.csv.write_row(row + values)
        return base_values


CompressScript("results.csv").run()
