import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase


class APCAExample(ExamplesBase):
    def __init__(self):
        super(APCAExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/apca/"
        self.algorithm = "APCA"
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 1, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.arrows = []
        self.patches = []

        self.apca1("apca1.pdf", 1, 8)
        self.apca2("apca2.pdf", 2, 10)
        self.apca3("apca3.pdf", 3, 11)

    def apca1(self, filename, step, index):
        self.decoded = self.copy_decoded[0:8]
        self.plot_values = [{'x_values': [0,7], 'y_values': [2,2]}]
        self.arrows = [{'x': 7, 'y': 2, 'touch_below': True}]
        self.patches = [{'point': (0, 1), 'w': 7, 'h': 2}]
        self.common(filename, step, index)

    def apca2(self, filename, step, index):
        self.decoded = self.copy_decoded[0:10]
        self.plot_values.append({'x_values': [8,9], 'y_values': [3,3]})
        self.arrows = [{'x': 9, 'y': 3, 'touch_above': True}]
        self.patches = [{'point': (8, 2), 'w': 1, 'h': 2}]
        self.common(filename, step, index)

    def apca3(self, filename, step, index):
        self.decoded = self.copy_decoded[0:12]
        self.plot_values.append({'x_values': [10,11], 'y_values': [1,1]})
        self.arrows = [{'x': 11, 'y': 1, 'touch_above': True, 'touch_below': True}]
        self.patches = [{'point': (10, 0), 'w': 1, 'h': 2}]
        self.common(filename, step, index)


APCAExample()
