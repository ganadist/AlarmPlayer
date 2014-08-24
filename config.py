import datetime
import json
import os
from lib import hms2time

CONFIG_FILE = 'config.json'
FETCH_TIME = None
CACHE_DIR = 'cache'
TIMETABLE_URL = ''
SOUND_URL = ''
DEFAULT_ALARM = ''


def load():
    global TIMETABLE_URL, SOUND_URL, FETCH_TIME, CACHE_DIR
    config = json.load(open(CONFIG_FILE))
    UUID = open('/sys/class/net/eth0/address').readline().strip().replace(':', '')
    TIMETABLE_URL = str(config.get('timetable_url')) + '?uuid=' + UUID
    SOUND_URL = str(config.get('sound_url')) + '?uuid=' + UUID
    FETCH_TIME = hms2time(config.get('time'))
    CACHE_DIR = str(config.get('cachedir'))
    try:
        os.makedirs(CACHE_DIR)
    except OSError:
        pass

if __name__ == '__main__':
    load()
    print CONFIG_FILE
    print FETCH_TIME
    print CACHE_DIR
