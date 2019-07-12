import sys
sys.path.append('.')


class PlotConstants(object):
    ALGORITHMS = ["CoderPCA", "CoderAPCA", "CoderCA", "CoderPWLH", "CoderPWLHInt", "CoderGAMPSLimit"]
    THRESHOLDS = [0, 1, 3, 5, 10, 15, 20, 30]
    WINDOWS = [4, 8, 16, 32, 64, 128, 256]

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
    COLOR_GREEN_F = 'forestgreen'

    COMPRESSION_RATIO = r'Tasa de compresi$\acute{o}$n (%)' # 'Tasa de compresion (%)'
    RELATIVE_DIFF = 'Diferencia relativa'
    ERROR_THRE = 'Umbral de error (%)'
