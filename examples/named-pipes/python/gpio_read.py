#!/usr/bin/env python3
"""Read digital inputs (GPIO) from the rexgend named pipe.

usage: ./gpio_read.py

Each line:  (timestamp) <channel> <state>   e.g. "(1699999999) 0 1"
Digital I/O is READ-ONLY through rexgend (no GPIO output).

For acc/gyro/adc use the same code with a different path; the value is a float:
  /var/run/rexgen/acc/rx  /var/run/rexgen/gyro/rx  /var/run/rexgen/adc/rx
"""
import re
import sys

path = "/var/run/rexgen/dig/rx"
line_re = re.compile(r"\((?P<ts>\d+)\)\s+(?P<ch>\S+)\s+(?P<val>\S+)")

try:
    with open(path, "r") as fp:
        print(f"reading {path} ...")
        for line in fp:
            m = line_re.match(line)
            if not m:
                continue
            ts, ch, state = int(m["ts"]), m["ch"], int(m["val"])
            print(f"t={ts}  digital[{ch}] = {state}")
except FileNotFoundError:
    sys.exit(f"no pipe {path} (digital configured?)")
except KeyboardInterrupt:
    pass
