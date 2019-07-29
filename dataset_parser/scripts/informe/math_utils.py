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

    #
    # This is the equation I have defined in the pdf. TODO: always use this equation
    #
    @staticmethod
    def relative_difference(value1, value2, return_string=False):
        if value1 == value2:
            return 0
        result = float(value1 - value2)  # in general, value1 > value2
        result /= float(value1)
        result *= 100
        if not return_string:
            return result
        return "%0.2f" % result

    @staticmethod
    def average(lst):
        return sum(lst) / len(lst)
