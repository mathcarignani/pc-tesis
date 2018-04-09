import sys
sys.path.append('.')

import coders.pca.window_utils as window_utils


class LinearBucket(object):
    def __init__(self, params):
        # self.nan = "N"  # This is the value that represents nodata
        # self.error_threshold = params['error_threshold']
        # self.max_bucket_size = params['max_bucket_size']
        # self.clear()
        self.polygon = CPolygon()

    def check_eps_constraint(self):
        hull = self.polygon.get_convex_hull()
        size = hull.size
        if size < 2:
            return True

        width = self._get_max_distance_for_edge(hull.get_at(size - 1), hull.get_at(0))
        for i in xrange(1, width):
            width = self._get_max_distance_for_edge(hull.get_at(i-1), hull.get_at(i))


    def _get_distance(self, point, line):
        pass

    #
    # Calculate max distance form any point in hull to 2 points
    #
    def _get_max_distance_for_edge(self, point1, point2):
        pass


class CPolygon(object):
    def __init__(self):
        self.all_points = []  # order by X. allPoints[0] is left-most point & allPoints[length -1] is right-most point
        self.upper_points = []  # order by X
        self.lower_points = []  # order by X

        self.left_point = None
        self.right_point = None

        self.convex_hull = Hull()
        self.upper_hull = Hull()
        self.lower_hull = Hull()


class Hull(object):
    def __init__(self):
        self.points = []

    def get_at(self, index):
        pass

