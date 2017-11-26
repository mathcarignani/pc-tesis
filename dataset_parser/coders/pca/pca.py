class PCA(object):
    def __init__(self):
        # coder / decoder inputs
        self.ERROR_THRESHOLD = 15
        self.WINDOW_SIZE = 2