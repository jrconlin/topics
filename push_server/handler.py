import json
import os

import cyclone.web
from twisted.logger import Logger


class MainHandler(cyclone.web.RequestHandler):

    def initialize(self, args=None):
        self._settings = args

    log = Logger()

    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST")
        self.set_header("Access-Control-Allow-Headers",
                        ",".join(["content-type"]))
        self.set_header("Access-Control-Expose-Headers",
                        ",".join(["content-type"]))

    @cyclone.web.asynchronous
    def options(self):
        self.prepare()
        self.finish()

    head = options

    @cyclone.web.asynchronous
    def post(self):
        """Accept and log the push endpoint data

        """
        self.prepare()
        try:
            # make sure it's valid JSON, even if you don't do anything with it.
            body = json.loads(self.request.body)
            out = os.open(self._settings.storage,
                          os.O_RDWR|os.O_CREAT,
                          0644)
            self.log.info("Writing body: {}".format(body))
            os.write(out, self.request.body)
            os.close(out)
            self.write("Ok")
            self.log.info("Done!")
        except Exception as x:
            self.log.error(repr(x))
            self.set_status(400)
            self.write(repr(x) + "\n\n")
        self.finish()

    @cyclone.web.asynchronous
    def get(self):
        """Super simple, horribly insecure page server.

        """
        types = {"css": "text/css", "js": "application/json"}
        path = self.request.uri.split("/")[-1] or 'index.html'
        self.add_header("content-type",
                        types.get(path.split('.')[1], "text/html"))
        try:
            data = open(os.path.join("page", path)).read()
            self.write(data)
        except Exception as x:
            self.log.error(repr(x))
            self.set_status(500)
        self.finish()

