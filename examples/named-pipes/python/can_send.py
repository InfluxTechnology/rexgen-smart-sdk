#!/usr/bin/env python3
"""Transmit a CAN frame through a rexgend named pipe.

usage: ./can_send.py [bus] [ID_hex] [byte ...]
   e.g. ./can_send.py can0 153 AA BB CC DD EE FF 00 11
        ./can_send.py can0 1ABCDEF0 DE AD BE EF          # extended ID

TX line format:  <ts> canN [flags] <ID_hex> <dlc> b0 b1 ...
  <ts>     ignored by the daemon (it stamps the frame) -> use 0
  ID_hex   1-3 hex digits = standard, 4+ = extended
"""
import sys

bus = sys.argv[1] if len(sys.argv) > 1 else "can0"
can_id = sys.argv[2] if len(sys.argv) > 2 else "153"
data = sys.argv[3:] if len(sys.argv) > 3 else ["AA", "BB", "CC", "DD", "EE", "FF", "00", "11"]

path = f"/var/run/rexgen/{bus}/tx"
# <ts> <bus> <id> <dlc> <bytes...>   (add "[FB]" before <id> for CAN-FD+BRS)
line = f"0 {bus} {can_id} {len(data)} " + " ".join(data)

try:
    with open(path, "w") as fp:
        fp.write(line + "\n")
    print(f"sent on {bus}: {line}")
except FileNotFoundError:
    sys.exit(f"no pipe {path} (is rexgend running / {bus} tx configured?)")
