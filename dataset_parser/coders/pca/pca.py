from window import Window


class PCA(object):
    def __init__(self, none, params={}):
        self.error_threshold = params.get('error_threshold') or 0
        self.fixed_window_size = params.get('fixed_window_size') or 5
        self.window = Window(self.error_threshold, self.fixed_window_size, none)
