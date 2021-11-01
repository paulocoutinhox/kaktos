import time


# -----------------------------------------------------------------------------
def current_time():
    return round(time.time())


# -----------------------------------------------------------------------------
def current_milli_time():
    return round(time.time() * 1000)
