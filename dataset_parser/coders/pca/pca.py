from window import Window

class PCA(object):
    def __init__(self):
        # coder / decoder inputs
        self.error_threshold = 0
        self.fixed_window_size = 1
        self.window = Window(self.error_threshold, self.fixed_window_size)
