#!/usr/bin/env node
// Read CAN frames from a rexgend SocketCAN (vcan) interface.
//   usage: node can_read.js [can0|can1|can2|can3]
//
// Requires the "socketcan" package:  npm install socketcan
// Needs use_socketcan=1 in rexgend.conf.

let can;
try {
  can = require('socketcan');
} catch (e) {
  console.error('missing dependency: run "npm install socketcan"');
  process.exit(1);
}

const iface = process.argv[2] || 'can0';

let channel;
try {
  channel = can.createRawChannel(iface, true /* receive own messages? no; timestamps */);
} catch (e) {
  console.error(`cannot open ${iface} (use_socketcan=1 and ${iface} configured?) - ${e.message}`);
  process.exit(1);
}

channel.addListener('onMessage', (msg) => {
  // msg: { id, ext (bool), rtr, data (Buffer), ts_sec, ts_usec }
  const id = msg.id.toString(16).toUpperCase();
  const data = Buffer.from(msg.data).toString('hex').toUpperCase().match(/../g) || [];
  console.log(`${iface}  ${msg.ext ? 'ext' : 'std'}  0x${id}  [${msg.data.length}] ${data.join(' ')}`);
});

channel.start();
console.log(`reading ${iface} ...`);
