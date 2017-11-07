from parser_irkis import ParserIRKIS


class ParserVWC(ParserIRKIS):
    def __init__(self):
        super(ParserVWC, self).__init__()
        self.nodata = "-999.000000"

    # In the vwc files the header is only the first line.
    # EXAMPLE:
    # timestamp -10cm_A -30cm_A -50cm_A -80cm_A -120cm_A -10cm_B -30cm_B -50cm_B -80cm_B -120cm_B
    def _parse_header(self, line):
        s_line = line.split()
        self._parse_columns(s_line)
        self.parsing_header = False

        # The filename string is used for the plot legend.
        # ylim is the y axis range.

    def plot(self, filename):
        sensor_labels = ['A', 'B']
        for label in sensor_labels:
            columns = [col for col in self.df.columns if label in col]
            df_label = self.df[columns]  # filter columns
            title = 'Sensors with label ' + label + ' in ' + filename
            ax = df_label.plot(title=title, ylim=[0, 0.6])
            fig = ax.get_figure()
            fig.savefig(filename + '_' + label + '.png')
