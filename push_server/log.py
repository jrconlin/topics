import sys

from twisted.logger import (formatEventAsClassicLogText, globalLogPublisher)
from twisted.python import log


class LogObserver(log.FileLogObserver):

    def __init__(self):
        self._output = sys.stdout
        self._format = formatEventAsClassicLogText

    def __call__(self, event, *args, **kwargs):
        printable = {}
        output = self._format(event)

        self._output.write(output)


    def start(self):
        globalLogPublisher.addObserver(self)
