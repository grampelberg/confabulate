#
# Copyright(c) 2010, Thomas Rampelberg <thomas@saunter.org>
# All rights reserved.
#

"""Setup config for the confabulator!"""

__date__ = "%date%"
__version__ = "%version%"

import pkg_resources
import tornado.options
from tornado.options import define, options

def definitions():
    define('config_file', default=pkg_resources.resource_filename(
            'confabulate.data', 'dev.conf'), help="Configuration file.")
    define('debug', default=False, type=bool, help='Enable debug mode.')
    define('aws_key', help="The AWS key for your account.")
    define('aws_secret', help='The AWS secret for your account.')
    define('num_processes', help='The number of processes to run under.',
           default=None, type=int)
    # serve.py
    define('port', default=8080, type=int, help="Port to start listening on.")


def register():
    definitions()
    # This is somewhat of a hack. I want to potentially get the config file off
    # the command line, but let the command line override anything input there,
    # so it just gets run twice.
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(options.config_file)
