import datetime

def hms2time(hhmmss):
    h, m, s = hhmmss[:2], hhmmss[2:4], hhmmss[4:6]
    return datetime.time(int(h), int(m), int(s))

