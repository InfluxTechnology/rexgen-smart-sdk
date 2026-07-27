#!/usr/bin/env node
// Transmit a CAN frame through a rexgend named pipe.
//   usage: node can_send.js [bus] [ID_hex] [byte ...]
//     e.g. node can_send.js can0 153 AA BB CC DD EE FF 00 11
//          node can_send.js can0 1ABCDEF0 DE AD BE EF        # extended ID
//
// TX line format:  <ts> canN [flags] <ID_hex> <dlc> b0 b1 ...
//   <ts> ignored by the daemon -> use 0
//   ID_hex 1-3 hex = standard, 4+ = extended

const fs = require('fs');

const bus = process.argv[2] || 'can0';
const canId = process.argv[3] || '153';
const data = process.argv.length > 4
  ? process.argv.slice(4)
  : ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', '00', '11'];

const path = `/var/run/rexgen/${bus}/tx`;
// add "[FB] " before canId for CAN-FD+BRS
const line = `0 ${bus} ${canId} ${data.length} ${data.join(' ')}`;

try {
  fs.writeFileSync(path, line + '\n');              // one frame per write
  console.log(`sent on ${bus}: ${line}`);
} catch (e) {
  console.error(`cannot write ${path} (rexgend running / ${bus} tx configured?) - ${e.code}`);
  process.exit(1);
}
