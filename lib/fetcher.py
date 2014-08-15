import os
from eloop import Spawn, main

class Fetcher:
    def __init__(self, url, outname):
        self.url = url
        self.outname = outname
        self.tmpname = outname + '.tmp'
        self.proc = None

    def run(self, complete_cb = None, *args):
        if self.proc:
            raise RuntimeError

        self.complete_cb = complete_cb
        self.cb_args = args
        self.clean_tmp()
        cmd = 'curl', '-o', self.tmpname, self.url
        self.proc = Spawn(cmd, self.watch)

    def clean_tmp(self):
        if os.access(self.tmpname, os.R_OK):
            os.unlink(self.tmpname)

    def watch(self, pid, status):
        success = status == 0
        if success:
            try:
                if os.access(self.outname, os.R_OK):
                    os.unlink(self.outname)
                os.rename(self.tmpname, self.outname)
            except OSError:
                success = False

        if not success:
            self.clean_tmp()

        if self.complete_cb:
            self.complete_cb(success, self, *self.cb_args)
        self.proc = None

    def __del__(self):
        self.clean_tmp()
        self.proc = None

if __name__ == '__main__':
    url = 'https://android.googlesource.com/mirror/manifest/+/master/default.xml'
    def cb(success, fetcher, *args):
        print 'success =', success, 'filename =', fetcher.outname, 'args =', args

    f = Fetcher(url, 'manifest.xml')
    f.run(cb, 'fetch test', 1, 2, 3)
    main()
