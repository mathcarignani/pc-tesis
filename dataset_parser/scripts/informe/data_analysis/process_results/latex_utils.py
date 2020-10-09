

class LatexUtils:
    COLOR_COMMANDS = {
        'PCA': "cyan!20",
        'APCA': "green!20",
        'FR': "yellow!25",
        'GZIP': "orange!20",
        # 'PWLHInt': 'violet!25',
        # 'PWLH': 'violet!50',
        # 'CA': 'brown!20'
    }

    @staticmethod
    def print_commands():
        array = []
        for key, value in LatexUtils.COLOR_COMMANDS.items():
            cell_color = "\cellcolor{" + value + "}"
            command = r"\newcommand{" + LatexUtils.command_key(key) + "}{" + cell_color + "}"
            array.append(command)
        return array

    @staticmethod
    def coder_style(coder):
        if LatexUtils.COLOR_COMMANDS.get(coder):
            return LatexUtils.command_key(coder)
        return ""

    @staticmethod
    def command_key(key):
        return '\c' + key.lower()  # cpca, capca, cfr, cgzip

    @staticmethod
    def array_to_table_row(array, with_separator=True):
        if with_separator:
            table_row = ' & '.join(['{' + str(element) + '}' for element in array])
        else:
            table_row = ' & '.join([str(element) for element in array])
        table_row += r" \\\hline"
        return table_row
