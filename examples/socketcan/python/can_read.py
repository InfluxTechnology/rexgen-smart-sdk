#!/usr/bin/env python3
"""Read CAN frames from a rexgend SocketCAN (vcan) interface.

usage: ./can_read.py [can0|can1|can2|can3]

Uses only the Python standard library (socket + struct) -- no external deps.
Needs use_socketcan=1 in rexgend.conf. For a higher-level API, see python-can
(https://python-can.readthedocs.io): can.Bus(interface="socketcan", channel="can0").
"""
import socket
import struct
import sys

bus = sys.argv[1] if len(sys.argv) > 1 else "can0"

# struct can_frame { u32 can_id; u8 can_dlc; u8 __pad,__res0,__res1; u8 data[8]; }
CAN_FRAME_FMT = "=IB3x8s"          # 16 bytes
CAN_EFF_FLAG = 0x80000000
CAN_ERR_FLAG = 0x20000000
CAN_EFF_MASK = 0x1FFFFFFF
CAN_SFF_MASK = 0x000007FF

try:
    s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind((bus,))
except OSError as e:
    sys.exit(f"cannot bind {bus} (use_socketcan=1 and {bus} configured?) - {e}")

print(f"reading {bus} ...")
try:
    while True:
        frame = s.recv(16)
        can_id, dlc, data = struct.unpack(CAN_FRAME_FMT, frame)
        if can_id & CAN_ERR_FLAG:
            print(f"ERROR frame id=0x{can_id & CAN_EFF_MASK:08X}")
            continue
        extended = bool(can_id & CAN_EFF_FLAG)
        real_id = can_id & (CAN_EFF_MASK if extended else CAN_SFF_MASK)
        payload = data[:dlc]
        print(f"{bus}  {'ext' if extended else 'std'}  0x{real_id:X}  "
              f"[{dlc}] {payload.hex(' ').upper()}")
except KeyboardInterrupt:
    pass
