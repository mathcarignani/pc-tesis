import sys
sys.path.append('.')

from file_utils.text_utils.text_file_writer import TextFileWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.gzip_compare.gzip_results_parser import GzipResultsParser
from scripts.informe.data_analysis.process_results.latex_utils import LatexUtils

#
# TODO: clean up the script after the Experiments chapter is written
#
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

    def __init__(self, path, mode):
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

        # print("set_threshold_results => " + str(threshold_results))
        assert(len(threshold_results) == 3 + self.THRE_COUNT * 3)

        dataset_str = ''
        if self.current_dataset is not None:
            dataset_str = self.DATASET_MAP[self.current_dataset]
            self.current_dataset = None

        line_list = [dataset_str, threshold_results[2]]
        for i in range(self.THRE_COUNT):
            index_begin = 3 * (i + 1)  # 3, 6,  9, ...
            coder = threshold_results[index_begin]
            coder_style = LatexUtils.coder_style(coder)
            window_value = threshold_results[index_begin + 1]
            window_x = self.WINDOW_MAP[window_value] if not self.__without_window() else window_value
            cr = threshold_results[index_begin + 2]
            cr = format(cr, '.2f')
            threshold_list = self.two_columns(False, coder_style + cr, coder_style + str(window_x))

            line_list += threshold_list
        line = LatexUtils.array_to_table_row(line_list)
        self.__write_line(line)

    ####################################################################################################################

    def __write_line(self, line):
        self.file.write_line(line)

    def __print_start(self):
        self.__write_line(r"\begin{table}[h]")
        for line in LatexUtils.print_commands():
            self.__write_line(line)
        self.__write_line("\centering")
        self.__write_line(self.__legend_for_mode())
        self.__write_line(r"\hspace*{-2.1cm}\begin{tabular}{| l | l " + (self.__c_list_for_mode() * self.THRE_COUNT) + "}")
        self.__write_line("\cline{3-" + str(self.THRE_COUNT * self.__count_for_mode() + 2) + "}")
        self.__write_line(self.threshold_line())
        columns = self.two_columns(True)
        self.__write_line("{Dataset} & {Data Type}" + (columns * self.THRE_COUNT) + r" \\\hline\hline")

    @staticmethod
    def add_gzip_result(threshold_results, gzip_cr):
        # [None, None, 'Lat', 'PCA', 256, 100.03, 'PCA', 256, 100.03, ... ]
        current_index = 5
        last_index = len(threshold_results) - 1
        while current_index <= last_index:
            cr = threshold_results[current_index]
            if gzip_cr < cr:
                threshold_results[current_index] = gzip_cr
                threshold_results[current_index - 1] = 0  # no window value
                threshold_results[current_index - 2] = 'GZIP'
            elif gzip_cr == cr:
                raise ValueError
            current_index += 3



    def threshold_line(self):
        line = "\multicolumn{1}{c}{}& \multicolumn{1}{c|}{} "
        column = "& \multicolumn{" + str(self.__count_for_mode()) + "}{c|"
        for thre in ExperimentsUtils.THRESHOLDS:
            line += column + ("|" if thre != 30 else "") + "}{e = " + str(thre) + "} "
        line += r"\\\hline"
        return line

    def print_end(self):
        lines = [
            r"\end{tabular}",
            r"\caption{" + self.__caption_for_mode() + "}",
            r"\label{experiments:mask-results-overview" + self.__label_for_mode() + "}",
            r"\end{table}"
        ]
        for line in lines:
            self.__write_line(line)

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
        return "| c | c |"

    def __count_for_mode(self):
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
