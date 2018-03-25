import sys
sys.path.append('../')

from aux.python_utils import inverse_dict
from file_utils.text_utils.text_file_reader import TextFileReader


class Dataset:
    def __init__(self, dictionary):
        self.min, self.max, self.bits = int(dictionary['min']), int(dictionary['max']), int(dictionary['bits'])
        self.offset = -self.min
        self.nan = self.offset + self.max + 1


class DatasetUtils:
    #
    # path and filename to the CONSTANTS file
    #
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/aux"
    FILENAME = "CONSTANTS"

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
                    self._add_key_value(split_line, reading_dataset)
                elif len(split_line) == 3:
                    self._add_alphabet_values(split_line)
                else:
                    reading_dataset, reading_time_unit, reading_alphabets = [False] * 3

    def _add_key_value(self, split_line, reading_dataset):
        key, value = split_line
        value = int(value)
        if reading_dataset:
            self.constants['dataset_dictionary'][key] = value
        else:  # reading_time_unit
            self.constants['time_unit_dictionary'][key] = value

    def _add_alphabet_values(self, split_line):
        dataset_name, min_max, bits = split_line  # key_value = ["IRKIS", "[0,600]", "16"]
        min_value, max_value = min_max.replace("[", "").replace("]", "").split(",")
        self.constants['alphabets_dictionary'][dataset_name] = {'min': min_value, 'max': max_value, 'bits': bits}
