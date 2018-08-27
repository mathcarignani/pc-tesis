

#
# https://stackoverflow.com/a/483833/4547232
#
def inverse_dict(my_map):
    return {v: k for k, v in my_map.iteritems()}


def number_of_bits(n):
    return len('{:b}'.format(n))
