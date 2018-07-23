import json
import os

import cyclone.web
from twisted.logger import Logger


class MainHandler(cyclone.web.StaticFileHandler):

    def initialize(self, args=None, **kwargs):
        super(MainHandler, self).initialize(**kwargs)
        self._settings = args

    log = Logger()

    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST")
        self.set_header("Access-Control-Allow-Headers",
                        ",".join(["content-type"]))
        self.set_header("Access-Control-Expose-Headers",
                        ",".join(["content-type"]))

    def options(self, *args, **kwargs):
        pass

    @cyclone.web.asynchronous
    def post(self, *args, **kwargs):
        """Accept and log the push endpoint data

        """
        try:
            # make sure it's valid JSON, even if you don't do anything with it.
            body = json.loads(self.request.body)
            out = os.open(self._settings.storage,
                          os.O_RDWR|os.O_CREAT|os.O_TRUNC,
                          0644)
            # Log generates a false info because it can't format the event
            print("Writing body: {}".format(body))
            os.write(out, self.request.body)
            os.close(out)
            self.write("Ok")
            self.log.info("Done!")
        except Exception as x:
            self.log.error(repr(x))
            self.set_status(400)
            self.write(repr(x) + "\n\n")
        self.finish()
