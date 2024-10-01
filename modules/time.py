import time
from datetime import datetime


# -----------------------------------------------------------------------------
def current_time():
    return round(time.time())


# -----------------------------------------------------------------------------
def current_time_ms():
    return round(time.time() * 1000)


# -----------------------------------------------------------------------------
def current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------------------------------------------------------
def format_datetime(date_str, date_format):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime(date_format)
    except ValueError:
        return None
