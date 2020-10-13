import sys
sys.path.append('.')

from scripts.informe.examples.examples_base import ExamplesBase


class LinearExample(ExamplesBase):
    def __init__(self):
        super(LinearExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/linear/"
        self.algorithm = "PCA"
        self.arrows = []
        self.patches = []
        self.plot_original = False
        self.xlim_right = 5
        self.figsize = [4.3, 3.48]
        self.first_timestamp = 5

        self.encoded_points = [(0,1),(4,3.5)]
        self.original = [1, 2, 2, 3, 4]
        self.decoded = [1, 2, 2, 3, 4]
        self.plot_values = [
             {'x_values': [0,4], 'y_values': [1, 3.5]}
        ]
        self.common("linear.pdf", None, None, False)


LinearExample()
