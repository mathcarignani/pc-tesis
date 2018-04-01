class WindowFixed(object):
    def __init__(self, params):
        self.nan = "N"  # This is the value that represents nodata
        self.error_threshold = params['error_threshold']
        self.fixed_window_size = params['fixed_window_size']
        self.current_window, self.current_window_length = [], 0

    #
    # PRE: not self.is_full()
    #
    def add_value_2_output(self, value):
        self.current_window.append(value)
        self.current_window_length += 1

    def is_full(self):
        return self.current_window_length == self.fixed_window_size

    #
    # If the window condition holds it returns the constant, otherwise it returns data_array.
    #
    # PRE: len(data_array) == data_array_length
    #
    def add_2_output(self):
        if self.current_window_length < self.fixed_window_size:
            # This is a particular scenario that can only occur with the last rows
            res = self.convert_array(self.current_window)
        elif self.nan in self.current_window:
            if self.current_window.count(self.nan) == self.current_window_length:
                # If all the elements in the data_array are self.nan then we return that constant
                res = self.nan
            else:
                res = self.convert_array(self.current_window)
        else:
            res = self.check_condition()
        self.current_window, self.current_window_length = [], 0
        return res

    def check_condition(self):
        data_array = self.convert_array(self.current_window)
        min_val, max_val = min(data_array), max(data_array)
        # print min_val, max_val

        min_val_aux = min_val + abs(min_val)  # >= 0
        max_val_aux = max_val + abs(min_val)  # >= 0

        if max_val_aux - min_val_aux >= 2*self.error_threshold:  # condition does not hold
            return data_array

        # condition holds
        constant = min_val + max_val
        return constant if constant == 0 else constant / 2

    def convert_array(self, data_array):
        # print data_array
        return [val if val == self.nan else int(val) for val in data_array]
