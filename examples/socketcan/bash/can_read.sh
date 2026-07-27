#!/bin/sh
# Read CAN frames from a rexgend SocketCAN (vcan) interface using can-utils.
#   usage: ./can_read.sh [can0|can1|can2|can3]
#
# Needs: can-utils (candump). Needs use_socketcan=1 in rexgend.conf.

IF="${1:-can0}"

ip link show "$IF" >/dev/null 2>&1 || {
  echo "interface $IF not found (use_socketcan=1 and $IF configured?)" >&2
  exit 1
}

# -e also prints error frames; -t A adds absolute timestamps.
candump -e -t A "$IF"

# Other handy forms:
#   candump any                 # every can* interface at once
#   candump can0,153:7FF        # only ID 0x153
#   candump -l can0             # log to a file (candump-*.log)
