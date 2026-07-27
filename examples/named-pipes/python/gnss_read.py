#!/usr/bin/env python3
"""Read GNSS (GPS) channels from the rexgend named pipe.

usage: ./gnss_read.py

Each line:  (timestamp) <channel> <value>
  Latitude, Longitude    -> float degrees
  Altitude, Speed*, ...  -> float
  Datetime               -> int (Unix epoch seconds, UTC)
"""
import re
import sys

path = "/var/run/rexgen/gnss/rx"
line_re = re.compile(r"\((?P<ts>\d+)\)\s+(?P<ch>\S+)\s+(?P<val>\S+)")

try:
    with open(path, "r") as fp:
        print(f"reading {path} ...")
        for line in fp:
            m = line_re.match(line)
            if not m:
                continue
            ts, ch, val = int(m["ts"]), m["ch"], m["val"]
            value = int(val) if ch == "Datetime" else float(val)
            print(f"t={ts}  {ch:<18} {value}")

            # Example: keep a live fix
            # if ch == "Latitude":  lat = value
            # if ch == "Longitude": lon = value
except FileNotFoundError:
    sys.exit(f"no pipe {path} (GNSS configured?)")
except KeyboardInterrupt:
    pass
