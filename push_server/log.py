import sys

from twisted.logger import (formatEventAsClassicLogText, globalLogPublisher)
from twisted.python import log


class LogObserver(log.FileLogObserver):

    def __init__(self):
        self._output = sys.stdout
        self._format = formatEventAsClassicLogText

    def __call__(self, event, *args, **kwargs):
        self._output.write(unicode(self._format(event)))

    def start(self):
        globalLogPublisher.addObserver(self)