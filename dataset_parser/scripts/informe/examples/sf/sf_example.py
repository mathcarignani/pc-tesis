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
        self.decoded =  [0, 1, 1, 2, 2, 2, 3, 3, 4, 3, 2, 0]
        self.plot_values = [
             {'x_values': [0,8], 'y_values': [0.27,3.72]},
             {'x_values': [8,11], 'y_values': [3.72,0.386]},
        ]
        self.encoded_points = [(0,0.27),(8,3.72),(11,0.386)]
        self.common("sf.pdf", None, 11, False)


SFExample()
