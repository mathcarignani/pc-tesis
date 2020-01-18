import sys
sys.path.append('.')

import matplotlib.gridspec as gridspec

from scripts.informe.plot.plot_mapper import PlotMapper
from scripts.informe.plot.plot_utils import PlotUtils


class PdfPage(object):
    def __init__(self, panda_utils_0, panda_utils_3, filename, pdf_instance):
        self.panda_utils_0 = panda_utils_0
        self.panda_utils_3 = panda_utils_3
        self.filename = filename
        self.col_index = pdf_instance.col_index
        self.plots_options = pdf_instance.plot_options() or pdf_instance.PLOT_OPTIONS or {}
        self.fig, self.plt = PlotUtils.create_figure(pdf_instance.FIG_SIZE_H_V, filename + ' - col = ' + str(self.col_index))
        self.height_ratios = pdf_instance.HEIGHT_RATIOS

    def create(self, coders_array, plots_array, plots_matrix): #, subplot_spacing_w_h):
        plots_obj = {}
        for plot_key in plots_array:
            options = self.plots_options.get(plot_key) or {}
            plot_klass = PlotMapper.map(plot_key)
            plots = plot_klass.create_plots(coders_array, self.filename, self.panda_utils_0, self.panda_utils_3, self.col_index, options)
            plots_obj[plot_key] = plots

        self.__add_plots(plots_matrix, plots_obj)
        return self.fig, self.plt

    def __add_plots(self, plots_matrix, plots_obj):
        total_rows, total_columns = len(plots_matrix), len(plots_matrix[0])
        spec = gridspec.GridSpec(ncols=total_columns, nrows=total_rows, figure=self.fig, height_ratios=self.height_ratios)
        for row_index, row in enumerate(plots_matrix):
            if row is None:
                continue
            for col_index, matrix_entry in enumerate(row):
                ax = self.fig.add_subplot(spec[row_index, col_index])
                self.__add_plot(matrix_entry, ax, plots_obj, row_index, col_index)

    def __add_plot(self, matrix_entry, ax, plots_obj, row_index, col_index):
        coder_name, plot_key = matrix_entry
        if coder_name is not None:
            plot_instance = plots_obj[plot_key][coder_name]
            extra = {
                # 'show_title': row_index in [0, 3],
                # 'last_row': row_index == (self.total_rows - 1),
                'show_ylabel': col_index == 0,
                # 'last_column': col_index == (self.total_columns - 2)
            }
            plot_instance.plot2(ax, extra)
        else:
            plot_instance = plots_obj[plot_key]
            plot_instance.plot(ax)
