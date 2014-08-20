import os, signal
import weakref
from gi.repository import GLib
from log import Logger

class Timer:
    def __init__(self, timeout, cb, *cb_data):
        self.tag = GLib.timeout_add(timeout, cb, *cb_data)

    def __del__(self):
        GLib.source_remove(self.tag)

class Idle:
    def __init__(self, cb, *cb_data):
        self.tag = GLib.idle_add(cb, *cb_data)

    def __del__(self):
        GLib.source_remove(self.tag)

class Spawn:
    Log = Logger('Spawn')
    def __init__(self, argv, cb, *cb_data):
        self.Log.i('cmd = %s'%str(argv))
        self.cmd = argv
        self.exited = False
        flags = (GLib.SPAWN_SEARCH_PATH | GLib.SPAWN_DO_NOT_REAP_CHILD)
        self.pid, stdin, stdout, stderr = GLib.spawn_async(argv,
                flags=flags)
        self.cb = cb
        self.cb_data = cb_data
        def cb(pid, status, ref):
            spawn = ref()
            if spawn:
                spawn.watch(pid, status)
        self.tag = GLib.child_watch_add(self.pid, cb, weakref.ref(self))

    def watch(self, pid, status):
        self.Log.i('cmd = %s was exited with %d'%(str(self.cmd), status))
        self.exited = True
        self.cb(pid, status, *self.cb_data)

    def __del__(self):
        if not self.exited:
            self.Log.w('cmd = %s is still alive. try to terminate'%(str(self.cmd)))
            try:
                os.kill(self.pid, signal.SIGTERM)
                os.kill(self.pid, signal.SIGKILL)
            except OSError:
                pass
            self.cb(self.pid, 255, *self.cb_data)
        GLib.source_remove(self.tag)

def main():
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    Log = Logger('eloop')
    def test_cb(*args):
        Log.i('args = %s'%str(args))
        return True
    timer = Timer(1000, test_cb, 'timer', 1, 2)
    child = Spawn(('sleep', '2' ), test_cb, 'spawn', 'hello')
    #child = None
    main()
