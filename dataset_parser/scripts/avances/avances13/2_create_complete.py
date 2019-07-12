import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/"
path_raw = path + "1-raw/"
path_raw_mac = path_raw + "mac/"
path_raw_ubuntu = path_raw + "ubuntu/"
path_complete = path + "2-complete/"


class CreateComplete(object):
    def __init__(self, mask_mode):
        self.mask_mode = mask_mode
        self.str_mask_mode = str(mask_mode)
        self.input_file = self.get_input_file()
        self.input_gamps_file = self.get_input_gamps_file()
        self.input_nino_file = self.get_input_nino_file()
        self.output_file = self.get_output_file()

    #
    # BEGIN FILE METHODS
    #
    def get_input_file(self):
        input_filename = "results-mask-mode={}.csv".format(self.str_mask_mode)
        return CSVReader(path_raw_ubuntu, input_filename)

    def get_input_gamps_file(self):
        input_filename = "results-mask-mode={}-gamps.csv".format(self.str_mask_mode)
        return CSVReader(path_raw_ubuntu, input_filename)

    def get_input_nino_file(self):
        input_filename = "results-mask-mode={}-gamps-el-nino.csv".format(self.str_mask_mode)
        return CSVReader(path_raw_mac, input_filename)

    def get_output_file(self):
        output_filename = "complete-mask-mode={}.csv".format(self.str_mask_mode)
        return CSVWriter(path_complete, output_filename)

    def close_files(self):
        self.input_file.close()
        self.input_gamps_file.close()
        self.input_nino_file.close()
        self.output_file.close()
    #
    # END FILE METHODS
    #

    def generate_file(self):
        line_count = 1
        previous_filename = None

        while self.input_file.continue_reading:
            line = self.input_file.read_line()
            if line_count > 1 and len(line[1]) > 0:
                current_filename = line[1]
                if previous_filename == "el-nino.csv":
                    self.copy_el_nino_gamps()
                elif previous_filename is not None:
                    self.copy_other_gamps(previous_filename)
                previous_filename = current_filename
                print(current_filename)
            self.output_file.write_row(line)
            line_count += 1
        self.copy_other_gamps(previous_filename)
        self.close_files()

    def copy_other_gamps(self, filename):
        self.input_gamps_file.goto_row(0)
        copy_mode = False
        while self.input_gamps_file.continue_reading:
            line = self.input_gamps_file.read_line()
            if len(line[1]) > 0:  # filename, copy_mode can change
                if copy_mode:
                    return  # copy_mode = False
                elif line[1] == filename:
                    print(filename + " ---- gamps")
                    copy_mode = True
            elif copy_mode:
                self.output_file.write_row(line)

    def copy_el_nino_gamps(self):
        while self.input_nino_file.continue_reading:
            line = self.input_nino_file.read_line()
            if len(line[0]) == 0:  # skip first two lines
                self.output_file.write_row(line)

CreateComplete(0).generate_file()
CreateComplete(3).generate_file()
