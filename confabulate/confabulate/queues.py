#
# Copyright(c) 2010, Thomas Rampelberg <thomas@saunter.org>
# All rights reserved.
#

"""Translate incoming connections to SQS queries."""

__date__ = "%date%"
__version__ = "%version%"

from tornado.options import options
import tornado.web

import confabulate.interface

class CallbackHandler(tornado.web.RequestHandler):
    """Adds in the ability to do optional callbacks for any request."""

    def prepare(self):
        self.cb = self.get_argument('callback', '')
        if self.cb:
            self.write('%s(' % (self.cb,))

    def finish(self, chunk=None):
        if chunk is not None: self.write(chunk)
        if self.cb: self.write(')')
        tornado.web.RequestHandler.finish(self)

    def _serialize(self, resp_dict):
        self.finish(tornado.escape.json_encode(resp_dict))

class ListQueues(CallbackHandler):
    """List all the currently available queues."""

    @tornado.web.asynchronous
    def get(self):
        confabulate.interface.Connection(
            options.aws_key, options.aws_secret).list(self._serialize)

class QueueHandler(CallbackHandler):
    """A simple handler than converts incoming requests into SQS queries."""

    def get(self, name):
        pass

    def post(self):
        pass

    def delete(self):
        pass

