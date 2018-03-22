import sys
sys.path.append('../')

from file_utils.text_utils.text_file_reader import TextFileReader


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
                    self._add_key_value(split_line, action, reading_dataset)
                elif len(split_line) == 3:
                    self._add_alphabet_values(split_line)
                else:
                    reading_dataset, reading_time_unit, reading_alphabets = [False] * 3

    def dataset_value(self, key):
        return self.constants['dataset_dictionary'][key]

    def time_unit_value(self, key):
        return self.constants['time_unit_dictionary'][key]

    def alphabet_values(self, dataset_name):
        return self.constants['alphabets_dictionary'][dataset_name]

    ####################################################################################################################

    def _add_key_value(self, key_value, action, reading_dataset):
        key, value = key_value
        value = int(value)
        if action == 'decode':
            aux = key
            key, value = value, aux
        if reading_dataset:
            self.constants['dataset_dictionary'][key] = value
        else:  # reading_time_unit
            self.constants['time_unit_dictionary'][key] = value

    def _add_alphabet_values(self, split_line):
        dataset_name, min_max, bits = split_line  # key_value = ["IRKIS", "[0,600]", "16"]
        min_value, max_value = min_max.replace("[", "").replace("]", "").split(",")
        min_value, max_value = int(min_value), int(max_value)
        self.constants['alphabets_dictionary'][dataset_name] = {'min': min_value, 'max': max_value, 'bits': int(bits)}

