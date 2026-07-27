#!/usr/bin/env node
// Transmit a CAN frame on a rexgend SocketCAN (vcan) interface.
//   usage: node can_send.js [bus] [ID_hex] [hexdata]
//     e.g. node can_send.js can0 153 AABBCCDDEEFF0011
//          node can_send.js can0 1ABCDEF0 DEADBEEF        # extended ID
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
const idStr = process.argv[3] || '153';
const hex = process.argv[4] || 'AABBCCDDEEFF0011';

const id = parseInt(idStr, 16);
const ext = id > 0x7ff || idStr.length > 3;     // extended if >11 bits / >3 hex digits
const data = Buffer.from(hex, 'hex');

let channel;
try {
  channel = can.createRawChannel(iface);
  channel.start();
  channel.send({ id, ext, rtr: false, data });
} catch (e) {
  console.error(`cannot send on ${iface} (use_socketcan=1 and ${iface} configured?) - ${e.message}`);
  process.exit(1);
}

console.log(`sent on ${iface}: id=0x${id.toString(16).toUpperCase()} ${ext ? '(ext) ' : ''}data=${hex.toUpperCase()}`);
channel.stop();
