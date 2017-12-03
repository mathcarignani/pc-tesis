import sys
sys.path.append('../')

from coders.pca.window import Window


class APCA(object):
    def __init__(self, params={}):
        error_threshold = params.get('error_threshold') or 0
        max_window_size = params.get('max_window_size') or 50
        self.window = Window(error_threshold, None, max_window_size)