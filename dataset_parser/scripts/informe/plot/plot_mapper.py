import sys
sys.path.append('.')

from scripts.informe.plots.compression_ratio_plot import CompressionRatioPlot
from scripts.informe.plots.relative_difference_plot import RelativeDifferencePlot
from scripts.informe.plots.windows_plot import WindowsPlot
from scripts.informe.plots.stats import RelativeDifferenceStats, WindowsStats

class PlotMapper(object):
    DICT = {
        'compression': CompressionRatioPlot,
        'relative': RelativeDifferencePlot,
        'window': WindowsPlot,
        'relative_stats': RelativeDifferenceStats,
        'window_stats': WindowsStats
    }

    @staticmethod
    def map(key):
        return PlotMapper.DICT[key]
