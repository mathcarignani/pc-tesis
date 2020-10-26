import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase


class GAMPSExample(ExamplesBase):
    def __init__(self):
        super(GAMPSExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/gamps/"
        self.algorithm = "GAMPS"
        self.original = [1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 3, 3]
        self.decoded =  [1, 1, 2, 2, 3, 2, 2, 3, 4, 4, 3, 3]
        self.encoded_points = [(0,1), (1,1), (2,2), (3,2), (4,3), (5,4), (6,4), (7,3), (8,4), (9,4), (10,3), (11,3)]
        self.plot_values = []
        self.arrows = []
        self.patches = []

        self.label_orig = 'sample (column 1)'
        self.label_enco = 'sample (column 2)'
        self.label_deco = 'sample (column 3)'
        self.epsilon = 0

        self.gamps1("gamps1.pdf", 0, 11)
        self.gamps2("gamps2.pdf", 1, 11)


    def gamps1(self, filename, step, index):
        self.common(filename, step, index)

    def gamps2(self, filename, step, index):
        self.decoded =  [1, 1, 1, 1, 1, 2/3, 2/3, 1, 1, 1, 1, 1]
        self.encoded_points = [(0,1), (1,1), (2,1), (3,1), (4,1), (5,4/3), (6,4/3), (7,1), (8,1), (9,1), (10,1), (11,1)]

        self.label_orig = 'encoded sample (column 1)'
        self.label_enco = 'encoded sample (column 2)'
        self.label_deco = 'encoded sample (column 3)'
        self.common(filename, step, index)



GAMPSExample()
