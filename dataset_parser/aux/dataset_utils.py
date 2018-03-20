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

        reading_dataset, self.dataset_dictionary = False, {}
        reading_time_unit, self.time_unit_dictionary = False, {}

        while text_file.continue_reading:
            line = text_file.read_line().rstrip()
            print line
            if line == "#DATASET":
                reading_dataset = True
            elif line == "#TIME_UNIT":
                reading_time_unit = True
            elif reading_dataset or reading_time_unit:
                key_value = line.split('=')
                if len(key_value) == 2:
                    self._add_key_value(key_value, action, reading_dataset, reading_time_unit)
                else:
                    reading_dataset, reading_time_unit = False, False

    def dataset_value(self, key):
        return self.dataset_dictionary[key]

    def time_unit_value(self, key):
        return self.time_unit_dictionary[key]

    ####################################################################################################################

    def _add_key_value(self, key_value, action, reading_dataset, reading_time_unit):
        key, value = key_value
        value = int(value)
        if action == 'decode':
            aux = key
            key, value = value, aux
        if reading_dataset:
            self.dataset_dictionary[key] = value
        else:  # reading_time_unit
            self.time_unit_dictionary[key] = value