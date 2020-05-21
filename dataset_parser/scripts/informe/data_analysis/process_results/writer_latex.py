import sys
sys.path.append('.')

from file_utils.text_utils.text_file_writer import TextFileWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.gzip_compare.gzip_results_parser import GzipResultsParser


class WriterLatex(object):
    THRE_COUNT = len(ExperimentsUtils.THRESHOLDS)
    DATASET_MAP = {
        'IRKIS': '\datasetirkis',
        'NOAA-SST': '\datasetsst',
        'NOAA-ADCP': '\datasetadcp',
        'SolarAnywhere': '\datasetsolar',
        'ElNino': '\datasetelnino',
        'NOAA-SPC-hail': '\datasethail',
        'NOAA-SPC-tornado': '\datasettornado',
        'NOAA-SPC-wind': '\datasetwind'
    }
    WINDOW_MAP = {0: '', 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8}
    WITH_C = False
    COLOR_COMMANDS = {
        'PCA': "\cellcolor{cyan!20}",
        'APCA': "\cellcolor{green!20}",
        'FR': "\cellcolor{yellow!25}",
        'GZIP': "\cellcolor{orange!20}",
        'PWLHInt': '\cellcolor{violet!25}',
        'PWLH': '\cellcolor{violet!50}',
        'CA': '\cellcolor{brown!20}'
    }

    def __init__(self, path, extra_str, mode):
        self.mode = mode
        filename = "table-results-" + str(mode) + '.tex'
        self.file = TextFileWriter(path, filename)
        self.__print_start()
        self.current_dataset, self.current_filename = None, None
        self.last_dataset, self.last_filename = None, None
        self.gzip = GzipResultsParser(True) if self.mode == 2 else None

    def set_dataset(self, dataset_name):
        # print "set_dataset => " + dataset_name
        self.current_dataset = dataset_name
        self.last_dataset = dataset_name

    def set_filename(self, filename):
        # print "set_filename => " + filename
        self.current_filename = filename
        self.last_filename = filename

    def set_threshold_results(self, threshold_results):
        # [None, None, 'Lat', 'PCA', 256, 100.03, 'PCA', 256, 100.03, 'APCA', 4, 88.74, 'APCA', 4, 81.29, 'APCA', 4, 69.82, 'APCA', 8, 62.44, 'APCA', 8, 56.18, 'APCA', 8, 47.15]
        col_name = threshold_results[2]
        # print "col_name => " + col_name
        if self.gzip is not None:
            gzip_cr = self.gzip.compression_ratio(self.last_dataset, self.last_filename, col_name)
            self.add_gzip_result(threshold_results, gzip_cr)

        # print "set_threshold_results => " + str(threshold_results)
        assert(len(threshold_results) == 3 + self.THRE_COUNT * 3)

        dataset_str = ''
        if self.current_dataset is not None:
            dataset_str = self.DATASET_MAP[self.current_dataset]
            self.current_dataset = None

        line_list = [dataset_str, threshold_results[2]]
        for i in range(self.THRE_COUNT):
            index_begin = 3 * (i + 1)  # 3, 6,  9, ...
            # print threshold_results
            # print index_begin
            coder = threshold_results[index_begin]
            if coder == "=":
                assert(threshold_results[index_begin:index_begin + 3] == ["=", "=", "="])
                line_list += ([" ", " ", " "] if self.WITH_C else [" ", " "])
                continue
            coder_style = self.coder_style(coder)
            window_value = threshold_results[index_begin + 1]
            window_x = self.WINDOW_MAP[window_value] if not self.__without_window() else window_value
            cr = threshold_results[index_begin + 2]
            if self.WITH_C:
                coder_with_style = coder_style + coder
                cr = "\cellcolor{red!10}" + str(cr) if cr >= 100 else str(cr)
                threshold_list = [coder_with_style, window_x, cr]
                assert(len(threshold_list) == 3)
            else:
                cr = "\color{red}" + str(cr) if cr >= 100 else str(cr)
                cr_with_style = coder_style + str(cr)
                window_with_style = coder_style + str(window_x)
                threshold_list = self.two_columns(False, cr_with_style, window_with_style)
            line_list += threshold_list
        line = ' & '.join(['{' + str(element) + '}' for element in line_list]) + r" \\\hline"
        self.__write_line(line)

    ####################################################################################################################

    def __write_line(self, line):
        self.file.write_line(line)

    def __print_start(self):
        self.__write_line(r"\begin{table}")
        self.__print_commands()
        self.__write_line("\centering")
        self.__write_line(self.__legend_for_mode())
        self.__write_line(r"\hspace*{-2.1cm}\begin{tabular}{| l | l " + (self.__c_list_for_mode() * self.THRE_COUNT) + "}")
        self.__write_line("\cline{3-" + str(self.THRE_COUNT * self.__count_for_mode() + 2) + "}")
        self.__write_line(self.threshold_line())
        columns = self.two_columns(True)
        if self.WITH_C:
            columns = r" & {c}" + columns
        self.__write_line("{Dataset} & {Data Type}" + (columns * self.THRE_COUNT) + r" \\\hline\hline")

    def __print_commands(self):
        for key, value in self.COLOR_COMMANDS.items():
            command = r"\newcommand{" + self.command_key(key) + "}{" + value + "}"
            self.__write_line(command)

    @staticmethod
    def add_gzip_result(threshold_results, gzip_cr):
        # [None, None, 'Lat', 'PCA', 256, 100.03, 'PCA', 256, 100.03, ... ]
        current_index = 5
        last_index = len(threshold_results) - 1
        while current_index <= last_index:
            coder = threshold_results[current_index - 2]
            if coder == '=':
                current_index += 3
                continue

            cr = threshold_results[current_index]
            if gzip_cr < cr:
                threshold_results[current_index] = gzip_cr
                threshold_results[current_index - 1] = 0  # no window value
                threshold_results[current_index - 2] = 'GZIP'
            elif gzip_cr == cr:
                raise ValueError
            current_index += 3

    def coder_style(self, coder):
        if coder not in ['PCA', 'APCA', 'FR', 'GZIP', 'PWLHInt', 'CA', 'PWLH']:
            print(coder)
            raise ValueError
        return WriterLatex.command_key(coder)

    def threshold_line(self):
        line = "\multicolumn{1}{c}{}& \multicolumn{1}{c|}{} "
        column = "& \multicolumn{" + str(self.__count_for_mode()) + "}{c|"
        for thre in ExperimentsUtils.THRESHOLDS:
            line += column + ("|" if thre != 30 else "") + "}{e = " + str(thre) + "} "
        line += r"\\\hline"
        return line

    @staticmethod
    def command_key(key):
        return '\c' + key.lower()  # cpca, capca, cfr, cgzip

    def print_end(self):
        self.__write_line("\end{tabular}")
        self.__write_line("\caption{" + self.__caption_for_mode() + "}")
        self.__write_line("\label{experiments:mask-results-overview" + self.__label_for_mode() + "}")
        self.__write_line(r"\end{table}")

    def two_columns(self, header = False, cr = None, w = None):
        if header:
            if self.__without_window():
                return r" & {\footnotesize CR} & {\footnotesize RD}"
            else:
                return r" & {\footnotesize CR} & {\footnotesize w}"
        return [cr, w]


    def __caption_for_mode(self):
        if self.gzip:
            return "\captiontwo"
        elif self.mode == 61:
            return "CoderPWLHInt vs. BEST"
        elif self.mode == 62:
            return "CoderAPCA vs. BEST"
        elif self.mode == 63:
            return "CoderPCA vs. BEST"
        else:
            return "\captionone"

    def __label_for_mode(self):
        if self.gzip:
            return "2"
        elif self.mode == 5:
            return "3"
        else:
            return "1"

    def __c_list_for_mode(self):
        if self.WITH_C:
            return "| c | c | c |"
        else:
            return "| c | c |"

    def __count_for_mode(self):
        if self.WITH_C:
            return 3
        else:
            return 2

    def __legend_for_mode(self):
        if self.mode in [1, 61, 62, 63]:
            return "\legendsone"
        elif self.mode == 2:
            return "\legendstwo"
        else:
            return "\legendsfive"

    def __without_window(self):
        return self.mode in [5, 61, 62, 63]