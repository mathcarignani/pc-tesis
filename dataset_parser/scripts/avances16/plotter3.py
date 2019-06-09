import sys
sys.path.append('.')

from scripts.avances15.plotter2 import Plotter2


class Plotter3(object):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.plotter2_array = []

    def add_plotter(self, plotter2):
        assert(isinstance(plotter2, Plotter2))
        self.plotter2_array.append(plotter2)

    def close(self):
        print "Plotter3 close"
        print len(self.plotter2_array)
