import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase
from scripts.informe.examples.sf.sf_example import SFExample


class SFIntro(ExamplesBase):
    def __init__(self):
        super(SFIntro, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/sf_intro/"
        self.xlim_right = 5
        self.figsize = [4.1, 3.48]
        self.window = None

        self.algorithm = "SF"
        self.arrows = []
        self.patches = []
        self.original = [2, 2, 2, 1, 1]
        self.decoded =  []
        self.plot_values = []
        # SFExample.common_sf(self, "sf0.pdf", 0, 11)
        self.sf1("sf1.pdf", 1, 2)
        self.sf2("sf2.pdf", 2, 2)

    def sf1(self, filename, step, index):
        self.plot_values = [
            {'x_values': [0,2], 'y_values': [3,-1], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,2], 'y_values': [1,5], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows = [
            {'x': 0, 'y': 2, 'touch_above': True, 'touch_below': True, 'left': True},
            {'x': 1, 'y': 2, 'touch_above': True, 'touch_below': True}
        ]
        self.patches = [{'points': [(0.5,2), (2,5), (2,-1)], 'polygon': True}]
        self.xs = [1.45 + self.SMIN_MAR, 1.65 + self.SMAX_MAR]
        self.ys = [0, 4]
        self.words = ['SMin', 'SMax']
        self.plot_values.append({'x_values': [0.5,3], 'y_values': [2,2], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs += [0.30, 2.1, 3 + self.SMAX_MAR]
        self.ys += [1.90, 2.1, 2-0.1]
        self.words += ['I', 'E', '(I,E)']
        SFExample.common_sf(self, filename, step, index)

    def sf2(self, filename, step, index):
        [a.update({'alpha': self.ALPHA_LOW}) for a in self.plot_values]
        self.plot_values.pop()
        self.plot_values += [
            {'x_values': [0,3], 'y_values': [3,0], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,3], 'y_values': [1,4], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows.pop()
        self.arrows.append({'x': 2, 'y': 2, 'touch_above': True, 'touch_below': True})
        self.patches = [{'points': [(1,2), (3,4), (3,0)], 'polygon': True}]
        self.xs = [2.1, 3 + self.SMIN_MAR, 3 + self.SMAX_MAR, 1 + self.SMIN_MAR, 1 + self.SMAX_MAR]
        self.ys = [2.1, 0, 4, 0, 4]
        self.words = ['E', 'SMin', 'SMax', 'SMinOld', 'SMaxOld']
        SFExample.common_sf(self, filename, step, index)

SFIntro()