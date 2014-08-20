import logging
import logging.handlers

class Logger:
    def __init__(self, TAG):
        self.log = logging.getLogger(TAG)
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.StreamHandler())

    def d(self, fmt):
        self.log.debug(fmt)

    def e(self, fmt):
        self.log.error(fmt)

    def i(self, fmt):
        self.log.info(fmt)

    def w(self, fmt):
        self.log.warn(fmt)

    def wtf(self, fmt):
        self.log.critical(fmt)
