import sys
sys.path.append('../')

from coders.pca.window import Window


class APCA(object):
    def __init__(self):
        # coder / decoder inputs
        error_threshold = 0
        max_window_size = 20
        self.window = Window(error_threshold, None, max_window_size)