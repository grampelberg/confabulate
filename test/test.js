/*
 * Simple functional tests for confabulate.js
 *
 * Copyright(c) 2010 BitTorrent Inc.
 * License: ************
 *
 * Date: %date%
 * Version: %version%
 *
 */


$(document).ready(function() {
  var aws_queue = sqs('localhost:8080');
  $("#send :button").click(function() {
    var queue = $("#send .queue").val();
    var msg = $("#send .message").val();
    aws_queue.send(queue, msg, function(resp) {
      console.log(resp);
      $("#result").text(JSON.stringify(resp));
    });
  });
  $("#receive :button").click(function() {
    var queue = $("#receive .queue").val();
    aws_queue.recv(queue, function(resp) {
      $("#result").text(JSON.stringify(resp));
    });
  });
  $("#remove :button").click(function() {
    var queue = $("#remove .queue").val();
    var msg = $("#remove .message").val();
    aws_queue.send(queue, msg, function(resp) {
      console.log(resp);
      $("#result").text(JSON.stringify(resp));
    });
  });
  $("#list :button").click(function() {
    aws_queue.list(function(resp) {
      $("#result").text(JSON.stringify(resp));
    });
  });
});
