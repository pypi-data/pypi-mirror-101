import pytz
import datetime as dt

def round_10min(time):
    a, b = divmod(time.minute, 10)
    return dt.datetime(time.year, time.month, time.day, time.hour, a*10)


def local_to_utc(time, tz):
    if not time.tzname():
        time = tz.localize(time)
    return (time.astimezone(dt.timezone.utc))

def utc_to_local(time, tz):
    if not time.tzname():
        time = pytz.timezone('UTC').localize(time)
    return (time.astimezone(tz))