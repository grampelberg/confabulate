#
# Copyright(c) 2010, Thomas Rampelberg <thomas@saunter.org>
# All rights reserved.
#

"""Allow pluggable asynchronous requests to SQS via. object inheritance."""

__date__ = "%date%"
__version__ = "%version%"

import base64
import functools
import hashlib
import hmac
import json
import logging
import simpledb.simpledb
import time
import tornado.httpclient
import urllib
from xml.etree import cElementTree as ElementTree

import confabulate.utils

def generate_timestamp():
    return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())

def escape(s):
    return urllib.quote(s, safe='-_~')

def urlencode(d):
    if isinstance(d, dict):
        d = d.iteritems()
    return '&'.join(['%s=%s' % (escape(k), escape(v)) for k, v in d])

class Connection(object):

    signature_version = '2'
    signature_method = 'HmacSHA256'
    version = '2009-02-01'
    host = 'queue.amazonaws.com'

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def queue(self, cb, name):
        params = { 'Action': 'CreateQueue',
                   'QueueName': name }
        self._request('/', params)

    def list(self, cb, prefix=None):
        params = { 'Action': 'ListQueues' }
        if prefix:
            params['QueueNamePrefix'] = prefix
        self._request(cb, '/', params)

    def _request(self, cb, path, params):
        params.update({ 'AWSAccessKeyId': self.key,
                        'SignatureVersion': self.signature_version,
                        'SignatureMethod': self.signature_method,
                        'Version': self.version,
                        'Timestamp': generate_timestamp(),
                        })
        base = '\n'.join(['GET', self.host, path,
                          urlencode(sorted(params.iteritems()))])
        params['Signature'] = base64.b64encode(
            hmac.new(self.secret, base, hashlib.sha256).digest())
        tornado.httpclient.AsyncHTTPClient().fetch(
            'http://queue.amazonaws.com/?%s' % (urlencode(params),),
            functools.partial(self._resp, cb))

    def _resp(self, cb, resp):
        if not resp.error:
            cb(confabulate.utils.xml_to_dict(resp.body))

class Queue(object):

    def __init__(self, name, conn):
        pass

    def attributes(self):
        pass

    def delete(self):
        pass

    def send_message(self, message):
        pass

    def receive_message(self, limit=10):
        pass

    def delete_message(self, id):
        pass

    def change_message_visibility(self):
        pass
