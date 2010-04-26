===========
Confabulate
===========

This is a two part solution to fixing some of the issues inherent in using
Amazon's SQS service.

#. There is no way to use it in a cross domain manner, since the response is
   XML and JSONP isn't allowed. The confabulate server takes the XML responses
   from SQS, converts them into JSON and then wraps in the JSONP callback if so
   required by the response.

#. To use SQS from client's computers, you'd need to either include your AWS
   secret in the source or create an API that is only used for actually signing
   URLS. The confabulate server, since it sits between SQS and the client,
   automatically signs all the urls destined for SQS.

#. Outside of using your AWS secret key, there is no way to do any kind of
   authentication to use SQS as you'd like to do for a general browser based
   message passing architecture. Since the confabulate server uses standard
   server side processing, you can plug in any authentication scheme you'd
   like.

To make reuse of the confabulate server easy, some javascript libraries have
also been written. They're simply there to make picking up and using the server
as easy and straight forward as possible. Feel free to implement your own if
you so desire.

Server
~~~~~~

The server is currently written in python and tied very closely to Tornado. In
the future, it is possible that the actual interface library
(confabulate.interface) will be rewritten in a manner that allows easy reuse in
any python asynchronous frameworks (honestly, it'd be pretty easy to monkey
patch even now as the only thing it really depends on is Tornado's async curl
implementation).

Install/Running
***************

..

  python setup.py install

  python -m confabulate.serve --config_file=my_config_file.conf

API
***

A quick overview of the API:

- / - List all the available queues

- /queue_name - This isn't an actual route, but I'd like to mention something
  about queue names in general here. For any requests to a queue that doesn't
  exist, the error from SQS is caught and the queue is auto-created. Therefore,
  don't worry about calling create queue (or delete queue, honestly), just
  pretend the queues always exist.

- /queue_name/send - Send a message, you'll get a stripped down JSON version of
  the XML as a response.

- /queue_name/receive - Receive a message, you'll get a stripped down JSON
  version of the XML as a response. The default limit here is 10 messages, if
  you'd like to get more or less, pass limit as a query string parameter.

- /queue_name/delete - Delete a specific message, you'll get a stripped down
  JSON version of the XML as a response. 'id' is a required parameter here and
  it is the message handle for the actual message.

Configuration
*************

There are some required parameters. Toss these into a configuration file of the
format 'key = value' and use the --config_file option on the command line. The
required configuration is:

- aws_key - AWS key for the account you're using
- aws_secret - AWS secret for the account you're using
- sqs_base - The number of your account. This can be found by looking at
  created queue URLs and taking the bit out between the hostname and the queue
  name.

Javascript
~~~~~~~~~~

Take a look at the js/ directory. The confabulate.js file defines the sqs
object that provides all the functionality of SQS to a client's browser.
