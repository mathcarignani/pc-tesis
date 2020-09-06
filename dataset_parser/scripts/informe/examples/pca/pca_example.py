import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase


class PCAExample(ExamplesBase):
    def __init__(self):
        super(PCAExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/pca/"
        self.algorithm = "PCA"
        self.window = 4
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 1, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.arrows = []
        self.patches = []

        self.pca1("pca1.pdf", 0, 11)
        self.pca2("pca2.pdf", 1, 3)
        self.pca3("pca3.pdf", 2, 7)
        self.pca4("pca4.pdf", 3, 11)

    def pca1(self, filename, step, index):
        self.decoded = []
        self.common(filename, step, index)

    def pca2(self, filename, step, index):
        self.decoded = self.copy_decoded[0:4]
        self.plot_values = [{'x_values': [0,3], 'y_values': [1,1]}]
        self.arrows = [{'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True}]
        self.patches = [{'point': (0, 0), 'w': 3, 'h': 2}]
        self.common(filename, step, index)

    def pca3(self, filename, step, index):
        self.decoded = self.copy_decoded[0:8]
        self.plot_values.append({'x_values': [4,7], 'y_values': [2,2]})
        self.arrows = [{'x': 4, 'y': 2, 'touch_above': True}]
        self.patches = [{'point': (4, 1), 'w': 3, 'h': 2}]
        self.common(filename, step, index)

    def pca4(self, filename, step, index):
        self.decoded = self.copy_decoded[0:12]
        self.arrows = [{'x': 8, 'y': 2.5, 'touch_above': True, 'touch_below': True, 'touch_all': True}]
        self.patches = [{'point': (8, 1.5), 'w': 3, 'h': 2}]
        self.common(filename, step, index)

PCAExample()
