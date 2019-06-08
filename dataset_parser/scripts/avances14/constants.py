import sys
sys.path.append('.')


class Constants(object):
    ALGORITHMS = ["CoderPCA", "CoderAPCA", "CoderCA", "CoderPWLH", "CoderPWLHInt", "CoderGAMPSLimit"]
    THRESHOLDS = [0, 1, 3, 5, 10, 15, 20, 30]
    WINDOWS = [4, 8, 16, 32, 64, 128, 256]
    INDEX_FILENAME = 1
    INDEX_ALGORITHM = 3
    INDEX_THRESHOLD = 4
    INDEX_WINDOW = 6

    MAX_COLUMN_TYPES = 7  # ElNino

    COLOR_SILVER = 'silver'
    COLOR_BLUE = 'blue'
    COLOR_LIGHT_BLUE = 'dodgerblue'
    COLOR_RED = 'red'
    COLOR_WHITE = 'white'
    COLOR_GREEN = 'limegreen'
    COLOR_WHEAT = 'wheat'
    COLOR_BLACK = 'black'
    COLOR_YELLOW = 'gold'
