#!/usr/bin/env node
// Read CAN frames from a rexgend named pipe.
//   usage: node can_read.js [can0|can1|can2|can3]
//
// Each line:  (timestamp)  can0  [flags]  ID  [dlc] b0 b1 ... bN
//   flags: "" classic, "[F]" CAN-FD, "[FB]" CAN-FD+BRS
//   ID:    3 hex digits = standard, 8 hex digits = extended

const fs = require('fs');
const readline = require('readline');

const bus = process.argv[2] || 'can0';
const path = `/var/run/rexgen/${bus}/rx`;

const re = /\((\d+)\)\s+(\S+)\s+(?:\[(F|FB)\]\s+)?([0-9A-Fa-f]+)\s+\[(\d+)\]\s*([0-9A-Fa-f ]*)/;

const stream = fs.createReadStream(path);           // blocks/opens on the FIFO
stream.on('error', (e) =>
  console.error(`cannot open ${path} (rexgend running / ${bus} configured?) - ${e.code}`));

const rl = readline.createInterface({ input: stream });
console.log(`reading ${path} ...`);

rl.on('line', (line) => {
  const m = re.exec(line);
  if (!m) return;
  const [, ts, , flags, id, dlc, data] = m;
  const extended = id.length > 3;
  const fd = flags !== undefined;
  const brs = flags === 'FB';
  const bytes = data.trim() ? data.trim().split(/\s+/) : [];
  console.log(
    `t=${ts} id=0x${parseInt(id, 16).toString(16).toUpperCase()} ` +
    `${extended ? 'ext' : 'std'}${fd ? ' FD' : ''}${brs ? ' BRS' : ''} ` +
    `dlc=${dlc} data=${bytes.join(' ')}`);
});
