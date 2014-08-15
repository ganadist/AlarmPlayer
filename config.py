import datetime
import json
import os

CONFIG_FILE = 'config.json'
FETCH_TIME = None
CACHE_DIR = 'cache'
URL = ''
DEFAULT_ALARM = ''


def load():
    global URL, FETCH_TIME, CACHE_DIR
    config = json.load(open(CONFIG_FILE))
    URL = str(config.get('url'))
    time = [int(x) for x in config.get('time').split(':')]
    FETCH_TIME = datetime.time(*time)
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
