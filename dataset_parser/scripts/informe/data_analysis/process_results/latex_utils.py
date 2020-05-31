

class LatexUtils:
    @staticmethod
    def array_to_table_row(array):
        table_row = ' & '.join(['{' + str(element) + '}' for element in array]) + r" \\\hline"
        return table_row
