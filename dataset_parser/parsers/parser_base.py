class ParserBase(object):
    NO_DATA = "N"

    def __init__(self):
        self.parsing_header = True
        self.columns = []
        self.columns_length = 0
        self.asc_timestamp = True  # timestamp[row_i] > timestamp[row_j] if row_i > row_j

    # PRE: self.parsing_header
    def parse_header(self, line):
        self._parse_header(line)
        if not self.parsing_header:
            self._check_errors()  # Once the header has been parsed, check possible errors

    def parse_data(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _parse_header(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _map_value(self, value):
        raise NotImplementedError("This method must be implemented.")

    def _check_errors(self):
        # if self.nodata is None:
        #     raise StandardError("Finished parsing header and nodata value is unknown.")
        if self.date_format is None:
            raise StandardError("Finished parsing header and date_format is unknown")
        if self.columns_length == 0:
            raise StandardError("Finished parsing header and the columns are unknown")
