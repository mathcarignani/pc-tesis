import sys
sys.path.append('.')


class CSVConstants(object):
    INDEX_DATASET = 0
    INDEX_FILENAME = 1
    INDEX_NO_ROWS = 2
    INDEX_ALGORITHM = 3
    INDEX_THRESHOLD = 4
    INDEX_THRESHOLD_LIST = 5
    INDEX_WINDOW = 6
    INDEX_TOTAL_SIZE = 7
    INDEX_CR_PERCENTAGE = 8
    INDEX_DELTA_PERCENTAGE = 12

    @staticmethod
    def check_lines(line1, line2):
        assert(line1[CSVConstants.INDEX_ALGORITHM] == line2[CSVConstants.INDEX_ALGORITHM])
        assert(line1[CSVConstants.INDEX_THRESHOLD] == line2[CSVConstants.INDEX_THRESHOLD])
        assert(line1[CSVConstants.INDEX_WINDOW] == line2[CSVConstants.INDEX_WINDOW])
        assert(len(line1) == len(line2))

    @staticmethod
    def is_percentage_index(index):
        if index < CSVConstants.INDEX_CR_PERCENTAGE:
            return False
        else:
            return (index - CSVConstants.INDEX_CR_PERCENTAGE) % 4 == 0

    @staticmethod
    def is_column_percentage_index(index):
        if index <= CSVConstants.INDEX_DELTA_PERCENTAGE:
            return False
        else:
            return (index - CSVConstants.INDEX_DELTA_PERCENTAGE) % 4 == 0

    @staticmethod
    def is_column_index(index):
        if index <= CSVConstants.INDEX_DELTA_PERCENTAGE:
            return False
        else:
            return (index - (CSVConstants.INDEX_DELTA_PERCENTAGE - 1)) % 4 == 0
