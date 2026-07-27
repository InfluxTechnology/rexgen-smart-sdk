#!/usr/bin/env python3
"""Transmit a CAN frame on a rexgend SocketCAN (vcan) interface.

usage: ./can_send.py [bus] [ID_hex] [byte ...]
   e.g. ./can_send.py can0 153 AA BB CC DD EE FF 00 11
        ./can_send.py can0 1ABCDEF0 DE AD BE EF          # extended ID

Standard library only. Needs use_socketcan=1 in rexgend.conf.
"""
import socket
import struct
import sys

bus = sys.argv[1] if len(sys.argv) > 1 else "can0"
can_id = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x153
data = bytes(int(b, 16) for b in sys.argv[3:]) if len(sys.argv) > 3 \
    else bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x11])

CAN_FRAME_FMT = "=IB3x8s"          # struct can_frame, 16 bytes
CAN_EFF_FLAG = 0x80000000

# Extended ID if it does not fit in 11 bits, or was given as >3 hex digits.
if can_id > 0x7FF or (len(sys.argv) > 2 and len(sys.argv[2]) > 3):
    can_id |= CAN_EFF_FLAG

dlc = min(len(data), 8)
frame = struct.pack(CAN_FRAME_FMT, can_id, dlc, data[:8].ljust(8, b"\x00"))

try:
    s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind((bus,))
    s.send(frame)
except OSError as e:
    sys.exit(f"cannot send on {bus} (use_socketcan=1 and {bus} configured?) - {e}")

print(f"sent on {bus}: id=0x{can_id & 0x1FFFFFFF:X} dlc={dlc} "
      f"data={data[:dlc].hex(' ').upper()}")
