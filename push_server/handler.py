import json
import os

import cyclone.web
from twisted.logger import Logger

class MainHandler(cyclone.web.RequestHandler):

    def initialize(self, args):
        self._settings = args

    log = Logger()

    @cyclone.web.asynchronous
    def post(self):
        """Accept and log the push endpoint data

        """
        try:
            body = json.loads(self.request.body)
            out = os.open(self._settings.storage, "rw+")
            os.write(out, json.dumps(body))
            os.close()
        except Exception as x:
            self.log.error(x)

