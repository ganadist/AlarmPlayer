import datetime
from eloop import Timer, main

def delta_to_ms(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**3

class DailyScheduler:
    def __init__(self, time, cb, *args):
        self.date = datetime.date.today()
        self.time = time
        self.datetime = datetime.datetime.combine(self.date, self.time)
        self.cb = cb
        self.cb_args = args

        now = datetime.datetime.now()
        if now > self.datetime:
            self.date = self.date + datetime.timedelta(1)

        self.do_schedule()

    def run_callback(self):
        self.cb(*self.cb_args)
        self.date = self.date + datetime.timedelta(1)
        self.do_schedule()

    def do_schedule(self):
        schedule_datetime = datetime.datetime.combine(self.date, self.time)
        now = datetime.datetime.now()
        delta = schedule_datetime - now
        self.tag = Timer(delta_to_ms(delta), self.run_callback)

class OneshotScheduler:
    def __init__(self, timestamp, cb, *args):
        schedule = datetime.datetime.fromtimestamp(timestamp)
        now = datetime.datetime.now()
        delta = schedule - now
        if delta.days < 0:
            raise ValueError('invalid timestamp')

        # do not repeat timer
        def cb_wrap(*__args):
            cb(*__args)

        self.tag = Timer(delta_to_ms(delta), cb_wrap, *args)

if __name__ == '__main__':
    def cb(*args):
        print datetime.datetime.now()
        print 'hh', args
        return True
    time = datetime.time(10, 51, 10)
    d = DailyScheduler(time, cb, 'timer', 1, 2)
    main()
