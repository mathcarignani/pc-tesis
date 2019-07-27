import sys
sys.path.append('.')


class MathUtils(object):
    DEFAULT_PERCENTAGE_DECIMAL_PLACES = 2

    @staticmethod
    def calculate_percent(big, small):
        return MathUtils.calculate_percentage(big, small, MathUtils.DEFAULT_PERCENTAGE_DECIMAL_PLACES)

    @staticmethod
    def calculate_percentage(big, small, decimal_places):
        return round((float(small) / float(big)) * 100, decimal_places)

    @staticmethod
    def str_to_int(string):
        return int(string.replace(".", ""))

    @staticmethod
    def print_absolute_diff(value1, value2):
        if value1 > value2:
            return str(value1 - value2)
        else:
            return str(value2 - value1)

    @staticmethod
    def int_to_str(value):
        return "{:,}".format(value)

    @staticmethod
    def relative_diff(big, small):
        val = (float(big) / float(small))  # * 100
        val = "%0.2f" % val  # + "%"
        return val

    @staticmethod
    def average(lst):
        return sum(lst) / len(lst)
