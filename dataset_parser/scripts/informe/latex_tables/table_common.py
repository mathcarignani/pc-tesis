
import sys
sys.path.append('.')


class TableCommon(object):
    DATASETS_ORDER = ["IRKIS", "SST", "ADCP", "ElNino", "Solar", "Hail", "Tornado", "Wind"]

    @staticmethod
    def format_line(array):
        return "    " + " & ".join(array) + r" \\\hline"
