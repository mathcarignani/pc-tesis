import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils

class LatexUtils:
    DATASETS_ORDER = ["IRKIS", "SST", "ADCP", "ElNino", "Solar", "Hail", "Tornado", "Wind"]

    COLOR_COMMANDS = {
        'PCA': "cyan!20",
        'APCA': "green!20",
        'FR': "yellow!25",
        'GZIP': "orange!20",
        # 'PWLHInt': 'violet!25',
        # 'PWLH': 'violet!50',
        # 'CA': 'brown!20'
    }

    DATASET_MAP = {
        'IRKIS': '\datasetirkis',
        'SST': '\datasetsst',
        'ADCP': '\datasetadcp',
        'Solar': '\datasetsolar',
        'ElNino': '\datasetelnino',
        'Hail': '\datasethail',
        'Tornado': '\datasettornado',
        'Wind': '\datasetwind'
    }

    @staticmethod
    def get_dataset_key(dataset_name):
        key = LatexUtils.DATASET_MAP.get(dataset_name)
        if key:
            return key
        short_name = ExperimentsUtils.get_dataset_short_name(dataset_name)
        return LatexUtils.DATASET_MAP[short_name]

    @staticmethod
    def print_commands():
        array = []
        for key, value in LatexUtils.COLOR_COMMANDS.items():
            cell_color = "\cellcolor{" + value + "}"
            command = r"\newcommand{" + LatexUtils.command_key(key) + "}{" + cell_color + "}"
            array.append(command)
        return array

    @staticmethod
    def coder_style(coder):
        if LatexUtils.COLOR_COMMANDS.get(coder):
            return LatexUtils.command_key(coder)
        return ""

    @staticmethod
    def command_key(key):
        return '\c' + key.lower()  # cpca, capca, cfr, cgzip

    @staticmethod
    def array_to_table_row(array, with_separator=True):
        if with_separator:
            table_row = ' & '.join(['{' + str(element) + '}' for element in array])
        else:
            table_row = ' & '.join([str(element) for element in array])
        table_row += r" \\\hline"
        return table_row

    @staticmethod
    def format_line(array):
        return "    " + " & ".join(array) + r" \\\hline"

    @classmethod
    def thousands(cls, value):
        return str('{0:,}'.format(value))

    @classmethod
    def round(cls, value, round_=1):
        return str(round(value, round_))

    @classmethod
    def round_thousands(cls, value):
        rounded = round(value, 1)
        return str('{0:,}'.format(rounded))
