#
# Copyright(c) 2010, Thomas Rampelberg <thomas@saunter.org>
# All rights reserved.
#

"""Startup the server that presents the REST API for SQS access via. JSONP."""

__date__ = "%date%"
__version__ = "%version%"

import logging
import pkg_resources
import tornado.httpserver
import tornado.ioloop
from tornado.options import options
import tornado.web

import confabulate.config
import confabulate.queues

if __name__ == '__main__':
    confabulate.config.register()
    application = tornado.web.Application(
        [ (r'/', confabulate.queues.ListQueues),
          (r'/(\S+?)/send', confabulate.queues.SendMessage),
          (r'/(\S+?)/receive', confabulate.queues.ReceiveMessage),
          (r'/(\s+?)/delete', confabulate.queues.DeleteMessage),
          ],
        debug=options.debug,
        static_path=pkg_resources.resource_filename('confabulate', 'data'))
    server = tornado.httpserver.HTTPServer(application)
    server.bind(options.port)
    server.start(options.num_processes)
    tornado.ioloop.IOLoop.instance().start()
