/*
 * Interface for the confabulator server.
 *
 * Copyright(c) 2010 BitTorrent Inc.
 * License: ************
 *
 * Date: %date%
 * Version: %version%
 *
 * Implements the full confabulator API. The API is just a light wrapper around
 * Amazon's SQS. SQS by default basically requires that you use your AWS secret
 * key for each request. The confabulator server acts as the authoritative man
 * in the middle. In addition, SQS doesn't have a way to do jsonp for
 * cross-domain scripting, returns everything in XML and doesn't have a good
 * per-user way of doing authentication.
 *
 * Required:
 *    jquery
 *    underscore
 *    JSON (for IE)
 */

var sqs = function(host) { return new sqs.fn.init(host) };

sqs.fn = sqs.prototype = {
  method: 'http',
  init: function(host) {
    this.host = host;
    return this;
  },
  _request: function(queeue, action, data, cb) {
    $.ajax({
      url: this.method + '://' + host + '/' + queue + '/' + action,
      data: data,
      dataType: 'jsonp',
      success: cb
    });
  },
  send: function(to, msg, cb) {
    this._request(to, 'send', { message: JSON.stringify(msg) }, cb);
  },
  recv: function(from, cb) {
    _.compose(function(resp) {
      return _.map(resp.ReceiveMessageResult.Message, function(v) {
        v.body = JSON.parse(v.body[0]);
        return v;
      });
    }, cb);
    this._request(from, 'receive', { }, cb);
  },
  delete: function(from, id, cb) {
    this._request(from, 'delete', { id: id }, cb);
  }
};

sqs.fn.init.prototype = sqs.fn;
