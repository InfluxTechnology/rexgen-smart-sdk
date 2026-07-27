#!/bin/sh
# Read CAN frames from a rexgend named pipe.
#   usage: ./can_read.sh [can0|can1|can2|can3]
#
# Each line looks like:
#   (timestamp)  can0  [flags]  ID  [dlc] b0 b1 ... bN
# flags: "" classic, "[F]" CAN-FD, "[FB]" CAN-FD+BRS

BUS="${1:-can0}"
PIPE="/var/run/rexgen/$BUS/rx"

[ -p "$PIPE" ] || { echo "no pipe $PIPE (is rexgend running / $BUS configured?)" >&2; exit 1; }

# Simplest form: just stream it.
cat "$PIPE"

# Tip: filter or reshape with awk, e.g. only extended-ID frames:
#   cat "$PIPE" | awk '$3 ~ /^[0-9A-F]{8}$/'
