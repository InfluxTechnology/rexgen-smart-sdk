#!/bin/sh
# Transmit a CAN frame on a rexgend SocketCAN (vcan) interface using can-utils.
#   usage: ./can_send.sh [bus] [cansend-frame]
#     e.g. ./can_send.sh can0 153#AABBCCDDEEFF0011
#
# Needs: can-utils (cansend). Needs use_socketcan=1 in rexgend.conf.
#
# cansend frame syntax:
#   153#AABBCCDD           standard ID 0x153, data AA BB CC DD
#   12345678#DEADBEEF      extended ID (8-digit ID)
#   153##1.AABBCC...       CAN FD (## + 1 hex nibble of flags, then data)

IF="${1:-can0}"
FRAME="${2:-153#AABBCCDDEEFF0011}"

ip link show "$IF" >/dev/null 2>&1 || {
  echo "interface $IF not found (use_socketcan=1 and $IF configured?)" >&2
  exit 1
}

cansend "$IF" "$FRAME"
echo "sent on $IF: $FRAME"
