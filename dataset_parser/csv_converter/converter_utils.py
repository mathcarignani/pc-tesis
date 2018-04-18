DELTA_FORMAT = "%H:%M:%S"  # "01:00:00"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # "2010-10-01 00:00:00"


def format_timedelta(td, time_unit):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)

    if time_unit == 'minutes':
        if seconds != 0:
            raise StandardError("seconds must be 0 if time_unit == 'minutes'")
        return 60*hours + minutes

    elif time_unit == 'hours':
        if seconds != 0:
            raise StandardError("seconds must be 0 if time_unit == 'hours'")
        if minutes != 0:
            raise StandardError("minutes must be 0 if time_unit == 'hours'")
        return hours

    else:
        raise StandardError("Implement time_unit = " + time_unit)
