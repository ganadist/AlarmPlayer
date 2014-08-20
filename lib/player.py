from eloop import Spawn, main
from log import Logger

class Player:
    Log = Logger('player')
    def __init__(self, filename):
        cmd = 'play', filename
        self.proc = Spawn(cmd, self.watch)

    def watch(self, pid, status):
        self.Log.i('player is exited with %s'%status)

if __name__ == '__main__':
    p = Player('/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga')
    main()
