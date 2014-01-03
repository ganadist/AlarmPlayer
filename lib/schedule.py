import datetime
import weakref
from eloop import Timer, main

def delta_to_ms(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**3

class BaseScheduler:
    def __init__(self, cb, *args):
        self.cb = cb
        self.cb_args = args

    def setup(self, date, time):
        self.date = date
        self.time = time
        schedule_datetime = datetime.datetime.combine(self.date, self.time)

        now = datetime.datetime.now()
        if now > schedule_datetime:
            self.update_next_date()

        self.do_schedule()

    def update_next_date(self):
        raise NotImplementedError

    def run_callback(self):
        self.cb(*self.cb_args)
        self.update_next_date()
        self.do_schedule()

    def do_schedule(self):
        schedule_datetime = datetime.datetime.combine(self.date, self.time)
        now = datetime.datetime.now()
        delta = schedule_datetime - now
        print 'register schedule for', self.date, self.time
        def wrapper(ref):
            schedule = ref()
            if schedule:
                schedule.run_callback()
        self.tag = Timer(delta_to_ms(delta), wrapper, weakref.ref(self))

    def __del__(self):
        print 'unregister schedule for', self.date, self.time
        self.tag = None

class WeeklyScheduler(BaseScheduler):
    def __init__(self, weekday, time, cb, *args):
        # weekday 0: sunday
        # weekday 6: saturday
        BaseScheduler.__init__(self, cb, *args)

        # convert python weekday
        weekday -= 1
        weekday %= 7

        date = datetime.date.today()
        date += datetime.timedelta((weekday - date.weekday())%7)
        self.setup(date, time)

    def update_next_date(self):
        self.date = self.date + datetime.timedelta(7)

class DailyScheduler(BaseScheduler):
    def __init__(self, time, cb, *args):
        BaseScheduler.__init__(self, cb, *args)
        date = datetime.date.today()
        self.setup(date, time)

    def update_next_date(self):
        self.date = self.date + datetime.timedelta(1)

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
    time = datetime.time(22, 51, 10)
    #d = DailyScheduler(time, cb, 'timer', 1, 2)
    d = WeeklyScheduler(6, time, cb, 'timer', 1, 2)
    main()
