import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase


class FRExample(ExamplesBase):
    LABEL_DIS = 'displaced point'
    COLOR_DIS = 'magenta'
                    
    def __init__(self):
        super(FRExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/fr/"
        self.algorithm = "FR"
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [1, 1, 1, 2, 2, 2, 3, 3, 4, 3, 2, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.displaced_points = []
        self.displaced_plot_values = []
        self.arrows = []
        self.patches = []

        self.fr1("fr1.pdf", 1, 11)
        self.fr2("fr2.pdf", 2, 11)
        self.fr3("fr3.pdf", 3, 11)
        self.fr4("fr4.pdf", 4, 11)

    def fr1(self, filename, step, index):
        self.decoded = []
        self.plot_values = []
        self.displaced_points = [{'x': 0, 'y': 1}, {'x': 11, 'y': 1}]
        self.displaced_plot_values = [{'x_values': [0,11], 'y_values': [1,1]}]
        self.arrows = [
            {'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True},
            {'x': 11, 'y': 1, 'touch_above': True, 'touch_below': True}
        ]
        self.patches = [{'point': (0, 0), 'w': 11, 'h': 2}]
        self.common_fr(filename, step, index)

    def fr2(self, filename, step, index):
        self.decoded = []
        self.plot_values = []
        self.displaced_points.append({'x': 5, 'y': 2})
        self.displaced_plot_values = [
            {'x_values': [0,5], 'y_values': [1,2]},
            {'x_values': [5,11], 'y_values': [2,1]},
        ]
        self.arrows = [
            {'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True},
            {'x': 5, 'y': 2, 'touch_above': True, 'touch_below': True},
            {'x': 11, 'y': 1, 'touch_above': True, 'touch_below': True}
        ]
        self.patches = [
            {'points': [(0,0), (0,2), (5,3), (5,1)], 'polygon': True},
            {'points': [(5,1), (5,3), (11,2), (11,0)], 'polygon': True},
        ]
        self.common_fr(filename, step, index)

    def fr3(self, filename, step, index):
        self.decoded = []
        self.plot_values = []
        self.displaced_points.append({'x': 8, 'y': 4})
        self.displaced_plot_values = [
            {'x_values': [0,5], 'y_values': [1,2]},
            {'x_values': [5,8], 'y_values': [2,4]},
            {'x_values': [8,11], 'y_values': [4,1]},
        ]
        self.arrows = [
            {'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True},
            {'x': 5, 'y': 2, 'touch_above': True, 'touch_below': True},
            {'x': 8, 'y': 4, 'touch_above': True, 'touch_below': True, 'no_legend_above': True},
            {'x': 11, 'y': 1, 'touch_above': True, 'touch_below': True}
        ]
        self.patches = [
            {'points': [(0,0), (0,2), (5,3), (5,1)], 'polygon': True},
            {'points': [(5,1), (5,3), (8,5), (8,3)], 'polygon': True},
            {'points': [(8,3), (8,5), (11,2), (11,0)], 'polygon': True},
        ]
        self.common_fr(filename, step, index)

    def fr4(self, filename, step, index):
        self.encoded_points = [(val['x'], val['y']) for val in self.displaced_points]
        self.decoded = self.copy_decoded[0:12]
        self.plot_values = self.displaced_plot_values
        self.displaced_points = []
        self.displaced_plot_values = []
        self.arrows = []
        self.patches = []
        self.common_fr(filename, step, index)

    def common_fr(self, filename, step, index):
        ax, fig = self.common_1(index)

        if len(self.displaced_points) > 0:
            FRExample.plot_displaced_points(ax, self.displaced_points)
            for p in self.displaced_plot_values:
                ax.plot(p['x_values'], p['y_values'], c=self.COLOR_DIS, zorder=1)

        self.common_2(ax, fig, step, True, filename)

    @classmethod
    def plot_displaced_points(cls, ax, displaced_points):
        x, y = [], []
        for displaced_point in displaced_points:
            x.append(displaced_point['x'])
            y.append(displaced_point['y'])
        ax.scatter(x, y, c=cls.COLOR_DIS, marker='o', zorder=2, alpha=cls.ALPHA_MED, label=cls.LABEL_DIS)
    

FRExample()
