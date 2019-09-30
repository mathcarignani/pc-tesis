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
        'GZIP': "\cellcolor{orange!20}"
    }

    def __init__(self, path, extra_str, with_gzip):
        filename = extra_str + '-process2-LATEX' + ('2' if with_gzip else '1') + '.txt'
        self.file = TextFileWriter(path, filename)
        self.__print_start()
        self.current_dataset, self.current_filename = None, None
        self.last_dataset, self.last_filename = None, None
        self.gzip_results_parser = GzipResultsParser(True) if with_gzip else None

    def __write_line(self, line):
        self.file.write_line(line)

    def __print_start(self):
        self.__write_line(r"\begin{sidewaystable}[ht]")
        self.__print_commands()
        self.__write_line("\centering")
        c_list = "| c | c | c |" if self.WITH_C else "| c | c |"
        count = 3 if self.WITH_C else 2
        self.__write_line(r"\begin{tabular}{| l | l " + (c_list * self.THRE_COUNT) + "}")
        self.__write_line("\cline{3-" + str(self.THRE_COUNT * count + 2) + "}")
        self.__write_line(WriterLatex.threshold_line())
        ows_cr = r" & {\footnotesize OWS} & {\footnotesize CR}"
        columns = r" & {c}" + ows_cr if self.WITH_C else ows_cr
        self.__write_line("{Dataset} & {Data Type}" + (columns * self.THRE_COUNT) + r" \\\hline\hline")

    def __print_commands(self):
        for key, value in self.COLOR_COMMANDS.iteritems():
            command = r"\newcommand{" + self.command_key(key) + "}{" + value + "}"
            self.__write_line(command)

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
        if self.gzip_results_parser is not None:
            gzip_cr = self.gzip_results_parser.compression_ratio(self.last_dataset, self.last_filename, col_name)
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
            window_x = self.WINDOW_MAP[threshold_results[index_begin + 1]]
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
                threshold_list = [window_with_style, cr_with_style]
                assert(len(threshold_list) == 2)
            line_list += threshold_list
        line = ' & '.join(['{' + str(element) + '}' for element in line_list]) + r" \\\hline"
        self.__write_line(line)

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
                raise StandardError
            current_index += 3

    @staticmethod
    def coder_style(coder):
        if coder not in ['PCA', 'APCA', 'FR', 'GZIP']:
            raise StandardError
        return WriterLatex.command_key(coder)

    @staticmethod
    def threshold_line():
        line = "\multicolumn{1}{c}{}& \multicolumn{1}{c|}{} "
        column = "& \multicolumn{" + ("3" if WriterLatex.WITH_C else "2") + "}{c|"
        for thre in ExperimentsUtils.THRESHOLDS:
            line += column + ("|" if thre != 30 else "") + "}{e = " + str(thre) + "} "
        line += r"\\\hline"
        return line

    @staticmethod
    def command_key(key):
        return '\c' + key.lower()  # cpca, capca, cfr, cgzip

    def print_end(self):
        self.__write_line("\end{tabular}")
        extra = "2" if self.gzip_results_parser else "1"
        self.__write_line("\caption{Mask results overview (" + extra + ").}")
        self.__write_line("\label{experiments:mask-results-overview" + extra + "}")
        self.__write_line(r"\end{sidewaystable}")