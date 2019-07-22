

#
# https://stackoverflow.com/a/483833/4547232
#
def inverse_dict(my_map):
    return {v: k for k, v in my_map.iteritems()}


def number_of_bits(n):
    return len('{:b}'.format(n))


#
# https://stackoverflow.com/a/46914500/4547232
#
def assert_equal_lists(list1, list2):
    assert all([a == b for a, b in zip(list1, list2)])
