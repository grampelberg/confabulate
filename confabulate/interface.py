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
from tornado.options import options
import urllib
import urlparse
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
    transport = 'http'
    host = 'queue.amazonaws.com'
    retry_length = 2

    def __init__(self, default_cb):
        self.key = options.aws_key
        self.secret = options.aws_secret
        self.default_cb = default_cb

    def queue(self, name):
        return Queue(name, self)

    def list(self, cb=None, prefix=None):
        params = { 'Action': 'ListQueues' }
        if prefix:
            params['QueueNamePrefix'] = prefix
        self._request('/', params)

    def _request(self, path, params, cb=None):
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
            '%s://%s%s?%s' % (self.transport, self.host, path,
                              urlencode(params),),
            functools.partial(self._resp, cb))

    # XXX - Need to filter SenderId out
    def _resp(self, cb=None, resp=None):
        if resp.error:
            if resp.error.code == 400:
                return self._error_handler(resp)
        json = confabulate.utils.xml_to_dict(resp.body)
        logging.info('aws.response', json)
        if not cb:
            return self.default_cb(json)
        return cb(json)

    def _error_handler(self, resp):
        codes = {
            "AWS.SimpleQueueService.NonExistentQueue": self._create_queue }
        body = confabulate.utils.xml_to_dict(resp.body)
        logging.info('aws.error\n%s' % (body,))
        for code in body['Error']['Code']:
            codes.get(code, self._error_default)(resp)

    def _error_default(self, resp):
        json = confabulate.utils.xml_to_dict(resp.body)
        logging.info('aws.error.unhandled\n%s' % (json,))
        return self.default_cb(json)

    def _create_queue(self, resp):
        self._request('/', {
                'Action': 'CreateQueue',
                'QueueName': urlparse.urlparse(
                    resp.request.url).path.rsplit('/', 1)[-1] },
                      functools.partial(self._complete_request,
                                        resp.request.url))

    def _complete_request(self, url, resp):
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time() + 2, functools.partial(
                tornado.httpclient.AsyncHTTPClient().fetch,
                url, functools.partial(self._resp, None)))

class Queue(object):

    def __init__(self, name, conn):
        self.conn = conn
        self.name = name
        self.path = '/%s/%s' % (options.sqs_base, self.name)
        self.url = '%s://%s%s' % (self.conn.transport,
                                  self.conn.host,
                                  self.path)

    def attributes(self):
        self.conn._request(self.path, { 'Action': 'GetQueueAttributes' })

    def delete(self):
        self.conn._request(self.path, { 'Action': 'DeleteQueue' })

    def send_message(self, message):
        self.conn._request(self.path, {
                'Action': 'SendMessage',
                'MessageBody': tornado.escape.url_escape(message) })

    def receive_message(self, limit=10):
        self.conn._request(self.path, { 'Action': 'ReceiveMessage',
                                        'MaxNumberOfMessages': str(limit)})

    def delete_message(self, id):
        self.conn._request(self.path, { 'Action': 'DeleteMessage',
                                        'ReceiptHandle': id })

    def change_message_visibility(self):
        pass
