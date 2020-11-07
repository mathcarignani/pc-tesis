import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase


class SFExample(ExamplesBase):
    def __init__(self):
        super(SFExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/sf/"
        self.algorithm = "SF"
        self.arrows = []
        self.patches = []
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  []
        self.plot_values = []
        self.common_sf("sf0.pdf", 0, 11)
        self.sf1("sf1.pdf", 1, 1)
        self.sf2("sf2.pdf", 2, 2)
        self.sf3("sf3.pdf", 3, 2)
        self.sf4("sf4.pdf", 4, 8)
        self.sf5("sf5.pdf", 5, 9)
        self.sf6("sf6.pdf", 6, 10)
        self.sf7("sf7.pdf", 7, 11)
        self.sf8("sf8.pdf", 8, 11)
        self.sf9("sf9.pdf", 9, 11)
        self.sf10("sf10.pdf", 10, 11)

    def sf1(self, filename, step, index):
        self.plot_values = [
            {'x_values': [0,1], 'y_values': [2,0], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,2], 'y_values': [0,4], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows = [
            {'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True, 'left': True},
            {'x': 1, 'y': 1, 'touch_above': True, 'touch_below': True}
        ]
        self.patches = [{'points': [(0.5,1), (2,4), (2,0), (1,0)], 'polygon': True}]
        self.xs = [1 + self.SMIN_MAR, 2 + self.SMAX_MAR]
        self.ys = [0, 4]
        self.words = ['SMin', 'SMax']
        self.common_sf(filename, step, index)

    def sf2(self, filename, step, index):
        # self.arrows.pop()
        self.plot_values.append({'x_values': [0.5,5], 'y_values': [1,1], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs += [2, 5 + self.SMAX_MAR]
        self.ys += [1, 1-0.1]
        self.words += ['E3', 'SE3']
        self.common_sf(filename, step, index)

    def sf3(self, filename, step, index):
        [a.update({'alpha': self.ALPHA_LOW}) for a in self.plot_values]
        self.plot_values.pop()
        self.plot_values += [
            {'x_values': [0,2], 'y_values': [2,0], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,3], 'y_values': [0,3], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows.pop()
        self.arrows.append({'x': 2, 'y': 1, 'touch_above': True, 'touch_below': True})
        self.patches = [{'points': [(1,1), (3,3), (3,0), (2,0)], 'polygon': True}]
        self.xs = [2 + self.SMIN_MAR, 3 + self.SMAX_MAR, 0.28 + self.SMIN_MAR, 2 + self.SMAX_MAR]
        self.ys = [0, 3, 0, 4]
        self.words = ['SMin', 'SMax', 'SMinOld', 'SMaxOld']
        self.common_sf(filename, step, index)

    def sf4(self, filename, step, index):
        self.plot_values = [
            {'x_values': [0,10], 'y_values': [1,(1/4)*10+1], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,9], 'y_values': [0,(1/2)*9], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,10], 'y_values': [2,2], 'color': self.COLOR_LINE, 'linestyle': ':', 'alpha': self.ALPHA_LOW},
        ]
        self.arrows = [
            {'x': 0, 'y': 1, 'touch_below': True, 'left': True, 'only_below': True},
            {'x': 4, 'y': 1, 'touch_above': True, 'left': True, 'only_above': True},
            {'x': 8, 'y': 4, 'touch_above': True, 'touch_below': True, 'no_legend_above': True},

        ]
        self.patches = [{'points': [(4,2), (10,(1/2)*10), (10, (1/4)*10+1) ], 'polygon': True}]
        self.xs = [10 + self.SMAX_MAR, 10 + self.SMAX_MAR, 9]
        self.ys = [3+0.5, 2-0.2, 4+0.2]
        self.words = ['SMin', 'SMinOld', 'SMax=SMaxOld']
        self.common_sf(filename, step, index)

    def sf5(self, filename, step, index):
        self.plot_values.pop()
        self.arrows[2]['only_below'] = True
        self.xs = [10 + self.SMAX_MAR, 9, 8.3, 10 + self.SMAX_MAR]
        self.ys = [3+0.5, 4+0.2, 1.9, 2-0.1]
        self.words = ['SMin', 'SMax', 'E10', 'SE10']
        self.encoded_points = [(0,0.27)]
        self.plot_values += [
            {'x_values': [0,10], 'y_values': [0.27,4.59], 'alpha': self.ALPHA_LOW},
            {'x_values': [4,10], 'y_values': [2,2], 'color': self.COLOR_LINE, 'linestyle': '--'}
        ]
        self.common_sf(filename, step, index)

    def sf6(self, filename, step, index):
        self.plot_values = [
            self.plot_values[2],
            {'x_values': [9,11], 'y_values': [1,3], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [9,10], 'y_values': [3,0], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows = [
            {'x': 9, 'y': 2, 'touch_above': True, 'touch_below': True, 'left': True},
            {'x': 9, 'y': 2, 'touch_above': True, 'touch_below': True, 'left': True},
            {'x': 10, 'y': 1, 'touch_above': True, 'touch_below': True}
        ]
        self.patches = [{'points': [(9.5, 1.5), (11,3), (11, 0), (10, 0)], 'polygon': True}]
        self.xs = [9 + self.SMIN_MAR, 10.55 + self.SMAX_MAR]
        self.ys = [0, 3]
        self.words = ['SMin', 'SMax']
        self.encoded_points = [(0,0.27)]
        self.common_sf(filename, step, index)

    def sf7(self, filename, step, index):
        self.plot_values.append({'x_values': [9.5,11.5], 'y_values': [1.5,0.8333], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs += [10.3, 11.03]
        self.ys += [0.9, 0.5]
        self.words += ['E12', 'SE12']
        self.common_sf(filename, step, index)

    def sf8(self, filename, step, index):
        [a.update({'alpha': self.ALPHA_LOW}) for a in self.plot_values]
        self.plot_values.pop()
        self.plot_values += [
            {'x_values': [9,11], 'y_values': [1,2], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [9,11], 'y_values': [3,0], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows.pop()
        self.arrows.append({'x': 11, 'y': 1, 'touch_above': True, 'touch_below': True})
        self.patches = [{'points': [(10, 1.5), (11,2), (11, 0)], 'polygon': True}]
        self.xs = [8.5 + self.SMIN_MAR, 10 + self.SMAX_MAR, 10.05, 10.5]
        self.ys = [0, 3, 0, 2.05]
        self.words = ['SMinOld', 'SMaxOld', 'SMin', 'SMax']
        self.common_sf(filename, step, index)

    def sf9(self, filename, step, index):
        self.plot_values.pop(1)
        self.plot_values.pop(1)
        self.plot_values[0] = {'x_values': [0,8], 'y_values': [0.27,3.72]}
        self.plot_values.append({'x_values': [8,11], 'y_values': [3.72,0.386]})
        for array in [self.xs, self.ys, self.words]:
            array.pop(0)
            array.pop(0)
        self.encoded_points = [(0,0.27),(8,3.72),(11,0.386)]
        self.common_sf(filename, step, index)

    def sf10(self, filename, step, index):
        self.decoded =  [0, 1, 1, 2, 2, 2, 3, 3, 4, 3, 2, 0]
        self.plot_values.pop(1)
        self.plot_values.pop(1)
        self.arrows = []
        self.patches = []
        self.xs, self.yx, self.words = [], [], []
        self.common_sf(filename, step, index)

    def common_sf(self, filename, step, index):
        ax, fig = self.common_1(index)
        self.plot_texts(ax)
        self.common_2(ax, fig, step, True, filename)

    def plot_texts(self, ax):
        for index, x in enumerate(self.xs):
            y = self.ys[index]
            s = self.words[index]
            color = 'black'
            if 'SM' in s or 'SE' in s:
                color = self.COLOR_LINE
            if s in ['A', 'S']:
                x -= 0.35
                y -= 0.06
            elif 'SMin' in s:
                if y == 0:
                    y += 0.05
            elif 'E' in s:
                if len(s) == 2:  # 'E1', 'E2', etc.
                    x -= 0.5
                    y -= 0.08
                else: # 'SE1', 'SE2', etc.
                    pass
            alpha = self.ALPHA_LOW if "Old" in s and "=" not in s else 1
            ax.text(x, y, s, fontsize=13, alpha=alpha, c=color)

SFExample()
