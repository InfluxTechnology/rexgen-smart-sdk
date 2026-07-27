#!/usr/bin/env node
// Read digital inputs (GPIO) from the rexgend named pipe.
//   usage: node gpio_read.js
//
// Each line:  (timestamp) <channel> <state>   e.g. "(1699999999) 0 1"
// Digital I/O is READ-ONLY through rexgend.
// For acc/gyro/adc use the same code with a different path (values are floats):
//   /var/run/rexgen/acc/rx  /var/run/rexgen/gyro/rx  /var/run/rexgen/adc/rx

const fs = require('fs');
const readline = require('readline');

const path = '/var/run/rexgen/dig/rx';
const re = /\((\d+)\)\s+(\S+)\s+(\S+)/;

const stream = fs.createReadStream(path);
stream.on('error', (e) => console.error(`cannot open ${path} (digital configured?) - ${e.code}`));

const rl = readline.createInterface({ input: stream });
console.log(`reading ${path} ...`);

rl.on('line', (line) => {
  const m = re.exec(line);
  if (!m) return;
  const [, ts, ch, state] = m;
  console.log(`t=${ts}  digital[${ch}] = ${parseInt(state, 10)}`);
});
