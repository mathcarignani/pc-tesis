from .. import parser_base
from .. import parser_extra
import pandas as pd


class ParserIRKIS(parser_base.ParserBase, parser_extra.ParserExtra):
    def __init__(self):
        super(ParserIRKIS, self).__init__()

    def _parse_header(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _parse_columns(self, s_line):
        # EXAMPLE:
        # fields       = timestamp TA TSS TSG VW DW VW_MAX ISWR OSWR ILWR PSUM HS RH
        columns = s_line[1:]
        # self.df = pd.DataFrame(columns=columns)
        # self.columns_count = len(self.df.columns)
        return columns

    def parse_data(self, line):
        # EXAMPLE:
        # 2009-10-01T01:00  279.26   275.43   275.43    1.1     0    0.0      0      0 271.947  0.000    0.000   1.000
        s_line = line.split()
        current_date = s_line[0]
        timestamp = pd.to_datetime(current_date)
        data = []
        for value in s_line[1:]:
            res = "N" if value == self.nodata else value
            data.append(res)
        return {'timestamp': timestamp, 'values': data}
