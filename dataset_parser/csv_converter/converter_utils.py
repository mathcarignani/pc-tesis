from datetime import datetime, timedelta
import pandas as pd

DELTA_FORMAT = "%H:%M:%S"  # "01:00:00"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # "2010-10-01 00:00:00"


def parse_datetime(datetime_str):
    return pd.to_datetime(datetime_str, format=DATE_FORMAT)


def parse_delta(delta_str):
    t = datetime.strptime(delta_str, DELTA_FORMAT)
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)


def timestamp_plus_delta(timestamp, delta):
    return timestamp + delta
