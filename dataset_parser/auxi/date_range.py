from datetime import datetime


class DateRange:
    DATE_FORMAT = "%m/%d/%Y %H:%M"

    def __init__(self, lower_bound_str=None, upper_bound_str=None):
        self.lower_bound_date = self.str_to_datetime(lower_bound_str)
        self.upper_bound_date = self.str_to_datetime(upper_bound_str)

    @classmethod
    def str_to_datetime(cls, datetime_str):
        return None if datetime_str is None else datetime.strptime(datetime_str, cls.DATE_FORMAT)

    def inside_range(self, dt):
        if self.lower_bound_date is None:
            if self.upper_bound_date is None:
                return True
            else:
                return dt <= self.upper_bound_date
        elif self.upper_bound_date is None:
            return self.lower_bound_date <= dt
        else:
            return self.lower_bound_date <= dt <= self.upper_bound_date
