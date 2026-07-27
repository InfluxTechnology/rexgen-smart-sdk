#!/usr/bin/env node
// Read GNSS (GPS) channels from the rexgend named pipe.
//   usage: node gnss_read.js
//
// Each line:  (timestamp) <channel> <value>
//   Latitude/Longitude -> float, Datetime -> int (Unix epoch s), rest -> float

const fs = require('fs');
const readline = require('readline');

const path = '/var/run/rexgen/gnss/rx';
const re = /\((\d+)\)\s+(\S+)\s+(\S+)/;

const stream = fs.createReadStream(path);
stream.on('error', (e) => console.error(`cannot open ${path} (GNSS configured?) - ${e.code}`));

const rl = readline.createInterface({ input: stream });
console.log(`reading ${path} ...`);

const fix = {};
rl.on('line', (line) => {
  const m = re.exec(line);
  if (!m) return;
  const [, ts, ch, val] = m;
  const value = ch === 'Datetime' ? parseInt(val, 10) : parseFloat(val);
  fix[ch] = value;
  console.log(`t=${ts}  ${ch.padEnd(18)} ${value}`);
});
