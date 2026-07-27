#!/usr/bin/env python3
"""Read CAN frames from a rexgend named pipe.

usage: ./can_read.py [can0|can1|can2|can3]

Each line:  (timestamp)  can0  [flags]  ID  [dlc] b0 b1 ... bN
  flags: "" classic, "[F]" CAN-FD, "[FB]" CAN-FD+BRS
  ID:    3 hex digits = standard, 8 hex digits = extended
"""
import re
import sys

bus = sys.argv[1] if len(sys.argv) > 1 else "can0"
path = f"/var/run/rexgen/{bus}/rx"

# (ts)  name  [flags]?   ID   [dlc]  bytes...
line_re = re.compile(
    r"\((?P<ts>\d+)\)\s+(?P<name>\S+)\s+(?:\[(?P<flags>F|FB)\]\s+)?"
    r"(?P<id>[0-9A-Fa-f]+)\s+\[(?P<dlc>\d+)\]\s*(?P<data>[0-9A-Fa-f ]*)"
)

try:
    with open(path, "r") as fp:            # blocks until rexgend is writing
        print(f"reading {path} ...")
        for line in fp:                    # one frame per line
            line = line.rstrip("\n")
            m = line_re.match(line)
            if not m:
                continue
            ts = int(m["ts"])
            can_id = int(m["id"], 16)
            extended = len(m["id"]) > 3
            fd = m["flags"] is not None
            brs = m["flags"] == "FB"
            data = bytes(int(b, 16) for b in m["data"].split())
            print(f"t={ts} id=0x{can_id:X} "
                  f"{'ext' if extended else 'std'}"
                  f"{' FD' if fd else ''}{' BRS' if brs else ''} "
                  f"dlc={int(m['dlc'])} data={data.hex(' ').upper()}")
except FileNotFoundError:
    sys.exit(f"no pipe {path} (is rexgend running / {bus} configured?)")
except KeyboardInterrupt:
    pass
