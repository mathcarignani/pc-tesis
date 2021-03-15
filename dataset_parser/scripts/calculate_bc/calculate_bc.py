import sys
sys.path.append('.')

import math
from auxi.os_utils import OSUtils
from file_utils.text_utils.text_file_reader import TextFileReader

class CalculateBc:
    INPUT_PATH = OSUtils.git_path() + "/dataset_parser/scripts/calculate_bc/"
    INPUT_FILENAME = "input.txt"
    @classmethod
    def run(cls):
        file = TextFileReader(cls.INPUT_PATH, cls.INPUT_FILENAME)
        while file.continue_reading:
            line = file.read_line()
            two_numbers = line.split("&")
            two_numbers = [int(s.replace(',', '')) for s in two_numbers]

            min_number, max_number = two_numbers
            bc = max_number - min_number
            if max_number != 131071:
                bc += 1

            bc = math.log2(bc)
            bc = math.ceil(bc)
            # print(min_number, max_number, bc)
            if max_number != 131071:
                print(bc)

CalculateBc.run()