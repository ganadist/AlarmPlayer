from eloop import Spawn, main

class Player:
    def __init__(self, filename):
        cmd = 'play', filename
        self.proc = Spawn(cmd, self.watch)

    def watch(self, pid, status):
        print 'player is exited with', status

if __name__ == '__main__':
    p = Player('/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga')
    main()
