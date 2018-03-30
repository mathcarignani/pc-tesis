class WindowFixed(object):
    def __init__(self, params):
        self.nan = "N"  # This is the value that represents nodata
        self.error_threshold = params['error_threshold']
        self.fixed_window_size = params['fixed_window_size']

    #
    # If the window condition holds it returns the constant, otherwise it returns data_array.
    #
    # PRE: len(data_array) == data_array_length
    #
    def add_2_output(self, data_array, data_array_length):
        if data_array_length < self.fixed_window_size:
            # This is a particular scenario that can only occur with the last lent(data_array) rows
            return self.convert_array(data_array)
        elif self.nan in data_array:
            if data_array.count(self.nan) == data_array_length:
                # If all the elements in the data_array are self.nan then we return that constant
                return self.nan
            else:
                return self.convert_array(data_array)
        else:
            data_array = self.convert_array(data_array)
            min_val, max_val = min(data_array), max(data_array)
            # print min_val, max_val
            constant = min_val + max_val
            return constant if constant == 0 else constant / 2

    def convert_array(self, data_array):
        # print data_array
        return [val if val == self.nan else int(val) for val in data_array]
