import sys
sys.path.append('.')

import os

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils


class GZipCompress(object):
    def __init__(self, dataset_name, filename, col_index, compress_path, transpose=True):
        self.dataset_name = dataset_name
        self.filename = filename
        self.col_index = col_index  # 1, 2, 3, ...
        self.transpose = transpose
        transpose_str = "-t" if transpose else ""
        self.compress_path = compress_path + "/c" + transpose_str + "/"

        # set filenames
        self.column_filename = filename + str(self.col_index) + transpose_str + ".csv"
        self.compressed_filename = self.column_filename + transpose_str + ".tar.gz"

    def total_size(self):
        if self.transpose:
            self.__create_column_csv_transpose()
        else:
            self.__create_column_csv()
        self.__compress_column_csv()
        total_bytes, total_bits = self.__read_total_size()
        self.__remove_files()
        return total_bytes, total_bits

    def __create_column_csv(self):
        dataset_columns_count, reader, writer = self.__common_create_column_csv()

        counter = 0
        while reader.continue_reading:
            row = reader.read_line()
            counter += 1
            if counter < 5:  # (1) REMOVE HEADER
                continue
            row.pop(0)  # (2) IGNORE TIME DELTA
            new_row = []
            for i, value in enumerate(row):
                # (3) APPEND VALUES FOR COLUMNS WITH THE MATCHING INDEX
                if i % dataset_columns_count == (self.col_index - 1):
                    new_row.append(row[i])
            writer.write_row(new_row)
        reader.close()
        writer.close()

    def __create_column_csv_transpose(self):
        dataset_columns_count, reader, writer = self.__common_create_column_csv()

        # (1) GET THE ROW INDEXES
        row_indexes = []
        counter = 0
        while reader.continue_reading:
            row = reader.read_line()
            counter += 1
            if counter < 5:  # (1) REMOVE HEADER
                continue
            row.pop(0)  # (2) IGNORE TIME DELTA
            for i, value in enumerate(row):
                # (3) APPEND INDEXES FOR COLUMNS WITH THE MATCHING INDEX
                if i % dataset_columns_count == (self.col_index - 1):
                    row_indexes.append(i)
            break
        print(len(row_indexes))
        print(row_indexes)

        # (2) WRITE THE FILES
        for index in row_indexes:
            reader.goto_row(0)
            counter = 0
            new_row = []
            while reader.continue_reading:
                row = reader.read_line()
                counter += 1
                if counter < 5:  # (1) REMOVE HEADER
                    continue
                row.pop(0)  # (2) IGNORE TIME DELTA
                new_row.append(row[index])
            writer.write_row(new_row)
        reader.close()
        writer.close()

    def __compress_column_csv(self):
        #
        # tar cvf - input_file_path/input_filename | gzip -9 - > input_file_path/input_filename.tar.gz
        #
        input_file_path = self.compress_path + self.column_filename
        output_file_path = self.compress_path + self.compressed_filename
        command = "tar cvf - " + input_file_path + " | gzip -9 - > " + output_file_path
        os.system(command)

    def __read_total_size(self):
        byte_size = os.path.getsize(self.compress_path + self.compressed_filename)
        bits_size = byte_size*8
        return byte_size, bits_size

    def __common_create_column_csv(self):
        dataset_columns_count = ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name)
        reader = CSVReader(ExperimentsUtils.get_dataset_path(self.dataset_name), self.filename)
        writer = CSVWriter(self.compress_path, self.column_filename)
        return dataset_columns_count, reader, writer

    def __remove_files(self):
        # pass
        os.remove(self.compress_path + self.column_filename)
        os.remove(self.compress_path + self.compressed_filename)
