import time


# -----------------------------------------------------------------------------
def current_time():
    return round(time.time())


# -----------------------------------------------------------------------------
def current_time_ms():
    return round(time.time() * 1000)
