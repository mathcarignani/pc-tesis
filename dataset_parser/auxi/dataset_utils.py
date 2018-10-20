import sys
sys.path.append('../')

from auxi.python_utils import inverse_dict
from auxi.os_utils import git_path
from file_utils.text_utils.text_file_reader import TextFileReader


class Dataset:
    def __init__(self, array):
        self.column_code_array = []
        for dictionary in array:
            column_code = ColumnCode(dictionary)
            self.column_code_array.append(column_code)
        self.column_code_array_length = len(self.column_code_array)
        self.current_column = None

    def set_column(self, column_index):
        if column_index == 0:  # time delta column
            array_index = 0
        else:  # data column
            array_index = column_index % (self.column_code_array_length - 1)
            if array_index == 0:
                array_index = self.column_code_array_length - 1
        column_code = self.column_code_array[array_index]
        self.current_column = column_code

        self.min, self.max, self.bits = column_code.min, column_code.max, column_code.bits
        self.offset = column_code.offset
        self.nan = column_code.nan

        # print column_number, array_index

    def get_bits(self):
        self.add_bits(self.bits)
        return self.bits

    def add_bits(self, bits):
        self.current_column.add_bits(bits)


class ColumnCode:
    def __init__(self, dictionary):
        self.min, self.max, self.bits = int(dictionary['min']), int(dictionary['max']), int(dictionary['bits'])
        self.offset = -self.min
        self.nan = self.offset + self.max + 1
        self.total_bits = 0

    def add_bits(self, bits):
        self.total_bits += bits


class DatasetUtils:
    #
    # path and filename to the CONSTANTS file
    #
    PATH = git_path() + "/constants"
    FILENAME = "CONSTANTS"  # "CONSTANTS"

    #
    # action can be 'code' or 'decode'
    #
    def __init__(self, action):
        self.action = action
        self._load_constants()

    def map_dataset(self, key):
        dictionary = self.constants['dataset_dictionary']
        dictionary = dictionary if self.action == 'code' else inverse_dict(dictionary)
        return dictionary[key]

    def map_time_unit(self, key):
        dictionary = self.constants['time_unit_dictionary']
        dictionary = dictionary if self.action == 'code' else inverse_dict(dictionary)
        return dictionary[key]

    def create_dataset_constants(self, dataset_name):
        return Dataset(self.constants['alphabets_dictionary'][dataset_name])

    ####################################################################################################################

    def _load_constants(self):
        text_file = TextFileReader(self.PATH, self.FILENAME)
        self.constants = {
            'dataset_dictionary': {},
            'time_unit_dictionary': {},
            'alphabets_dictionary': {}
        }
        reading_dataset, reading_time_unit, reading_alphabets = [False] * 3

        while text_file.continue_reading:
            line = text_file.read_line().rstrip()
            if line == "#DATASET":
                reading_dataset = True
            elif line == "#TIME_UNIT":
                reading_time_unit = True
            elif line == "#ALPHABETS":
                reading_alphabets = True
            elif reading_dataset or reading_time_unit or reading_alphabets:
                split_line = line.split('=')
                if len(split_line) == 2:
                    if reading_alphabets:
                        self._add_alphabet_values(split_line)
                    else:
                        self._add_key_value(split_line, reading_dataset)
                else:
                    reading_dataset, reading_time_unit, reading_alphabets = [False] * 3

    def _add_key_value(self, split_line, reading_dataset):
        key, value = split_line
        value = int(value)
        if reading_dataset:
            self.constants['dataset_dictionary'][key] = value
        else:  # reading_time_unit
            self.constants['time_unit_dictionary'][key] = value

    #
    # split_line examples:
    # ["IRKIS", "[0,600]"]
    # ["ElNino", "[-9000,9000],[-18000,18000],[0,4000]"]
    #
    def _add_alphabet_values(self, split_line):
        dataset_name, min_max_array = split_line
        min_max_array_split = min_max_array.split('],[')

        alphabet_values_array = []
        for idx, val in enumerate(min_max_array_split):
            min_value, max_value = val.replace("[", "").replace("]", "").split(",")
            alphabet_values_array.append({'min': min_value, 'max': max_value})

        self.constants['alphabets_dictionary'][dataset_name] = alphabet_values_array
