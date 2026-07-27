#!/bin/sh
# Transmit a CAN frame through a rexgend named pipe.
#   usage: ./can_send.sh [bus] ["<frame line>"]
#
# TX line format:  <ts> canN [flags] <ID_hex> <dlc> b0 b1 ...
#   <ts>     any integer, ignored (daemon stamps the frame)
#   [flags]  optional "[F]" (CAN-FD) or "[FB]" (CAN-FD+BRS)
#   <ID_hex> 1-3 hex digits = standard, 4+ = extended
#   <dlc>    number of data bytes

BUS="${1:-can0}"
FRAME="${2:-0 $BUS 153 8 AA BB CC DD EE FF 00 11}"
PIPE="/var/run/rexgen/$BUS/tx"

[ -p "$PIPE" ] || { echo "no pipe $PIPE (is rexgend running / $BUS tx configured?)" >&2; exit 1; }

printf '%s\n' "$FRAME" > "$PIPE"
echo "sent on $BUS: $FRAME"

# Examples:
#   ./can_send.sh can0 "0 can0 1ABCDEF0 4 DE AD BE EF"          # extended ID
#   ./can_send.sh can0 "0 can0 [FB] 12345678 12 00 01 02 03 04 05 06 07 08 09 0A 0B"  # CAN-FD+BRS
#
# Bridge one bus to another:
#   cat /var/run/rexgen/can0/rx > /var/run/rexgen/can1/tx
