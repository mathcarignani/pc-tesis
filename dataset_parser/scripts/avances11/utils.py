import sys
sys.path.append('.')


def calculate_percentage(big, small):
    return round((float(small) / float(big)) * 100, 2)


def to_int(value):
    return int(value.replace(".", ""))


def print_absolute_diff(value1, value2):
    if value1 > value2:
        return str(value1 - value2)
    else:
        return str(value2 - value1)


def int_to_str(value):
    return "{:,}".format(value)


def relative_diff(big, small):
    val = (float(big) / float(small))  # * 100
    val = "%0.2f" % val  # + "%"
    return val
