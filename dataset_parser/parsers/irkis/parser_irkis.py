from .. import parser_base
import numpy as np
import pandas as pd


class ParserIRKIS(parser_base.ParserBase):
    def __init__(self):
        super(ParserIRKIS, self).__init__()

    def _parse_header(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _parse_columns(self, s_line):
        # EXAMPLE:
        # fields       = timestamp TA TSS TSG VW DW VW_MAX ISWR OSWR ILWR PSUM HS RH
        self.df = pd.DataFrame(columns=s_line[1:])
        self.columns_count = len(self.df.columns)

    def _parse_data(self, line):
        # EXAMPLE:
        # 2009-10-01T01:00  279.26   275.43   275.43    1.1     0    0.0      0      0 271.947  0.000    0.000   1.000
        s_line = line.split()
        try:
            np_array = None
            current_date = s_line[0]
            timestamp = pd.to_datetime(current_date)
            data = s_line[1:]
            self._add_data(data, current_date, line, timestamp, np_array)

        except:
            self.errors['errors'].append(line)
