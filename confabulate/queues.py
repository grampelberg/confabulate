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

    def __init__(self, *args, **kwargs):
        self.conn = confabulate.interface.Connection(self._serialize)
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

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
        self.conn.list(self._serialize)

class SendMessage(CallbackHandler):
    """Send a message to SQS."""

    @tornado.web.asynchronous
    def get(self, name):
        self.conn.queue(name).send_message(self.get_argument('message'))

class ReceiveMessage(CallbackHandler):
    """Receive messages from a queue on SQS."""

    @tornado.web.asynchronous
    def get(self, name):
        self.conn.queue(name).receive_message(
            limit=str(self.get_argument('limit', '10')))

class DeleteMessage(CallbackHandler):
    """Delete a message from a queue on SQS."""

    @tornado.web.asynchronous
    def get(self, name):
        self.conn.queue(name).delete_message(self.get_argument('id'))

