import datetime


def to_days_diff(start, end):
    dt_start = datetime.datetime.strptime(start, '%Y%m%d')
    dt_end = datetime.datetime.strptime(end, '%Y%m%d')
    diff = dt_end - dt_start
    return diff.days


def to_date_after(base, days):
    dt_base = datetime.datetime.strptime(base, '%Y%m%d')
    dt_after = dt_base + datetime.timedelta(days=days)
    return dt_after.strftime('%Y%m%d')
