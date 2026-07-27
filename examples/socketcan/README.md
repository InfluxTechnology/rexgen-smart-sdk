# RexGEN smart — SocketCAN (vcan) Interface

Reference and examples for reading and writing RexGEN smart CAN traffic through
the `rexgend` **SocketCAN virtual interfaces**.

- [1. What it is](#1-what-it-is)
- [2. Why use it](#2-why-use-it)
- [3. Interfaces & mapping](#3-interfaces--mapping)
- [4. Enabling it](#4-enabling-it)
- [5. How rexgend wires it up](#5-how-rexgend-wires-it-up)
- [6. Receiving frames](#6-receiving-frames)
- [7. Transmitting frames](#7-transmitting-frames)
- [8. CAN FD](#8-can-fd)
- [9. Error frames](#9-error-frames)
- [10. Standard tools](#10-standard-tools)
- [11. Examples in this folder](#11-examples-in-this-folder)
- [12. Notes, limits, FAQ](#12-notes-limits-faq)

---

## 1. What it is

When SocketCAN mode is enabled, `rexgend` creates real Linux **virtual CAN
(`vcan`) network interfaces** named `can0`..`can3`. Frames received from the
RexGEN smart logger are injected into these interfaces, and frames you send to
them are extracted and transmitted by the device. From the application's point
of view they behave like any Linux CAN interface.

## 2. Why use it

- **Standard Linux CAN API.** Use `AF_CAN`/`SOCK_RAW`, `struct can_frame` /
  `struct canfd_frame` — the exact model every SocketCAN program expects.
- **Off-the-shelf tooling.** `candump`, `cansend`, `cangen`, `canplayer`,
  Python `python-can`, Wireshark, etc. work unchanged.
- **Binary & efficient.** No text formatting/parsing; better for high frame rates.
- **CAN FD.** FD frames (up to 64 data bytes) are supported.

For quick text/scripting, the named-pipe interface (`../named-pipes/`) may be
simpler; both are active at the same time when SocketCAN is enabled.

## 3. Interfaces & mapping

| Linux interface | Physical CAN bus |
|-----------------|------------------|
| `can0`          | CAN bus 0        |
| `can1`          | CAN bus 1        |
| `can2`          | CAN bus 2        |
| `can3`          | CAN bus 3        |

Names match the named-pipe channel names 1:1. An interface is created only if
that CAN bus is present in the loaded logger configuration.

Verify on the device:
```sh
ip -details link show can0
# ... link/can ... vcan ...
```

## 4. Enabling it

Config file `/data/rexgen/config/rexgend.conf`, section `[Live data]`:
```ini
[Live data]
use_socketcan = 1     ; 1 = create vcan interfaces (default), 0 = named pipes only
```
Then `systemctl restart rexgend`.

- `1` → vcan interfaces are created **in addition to** the CAN named pipes.
- `0` → no vcan interfaces; use the named pipes.

Sensors (GNSS, accelerometer, gyro, digital, ADC) are **not** exposed over
SocketCAN — read them from the named pipes (`../named-pipes/`).

## 5. How rexgend wires it up

- Interfaces are created with a Netlink `RTM_NEWLINK` using
  `IFLA_INFO_KIND = "vcan"` (standard kernel virtual CAN), and removed with
  `RTM_DELLINK` on reconfiguration.
- On each interface's socket rexgend enables `CAN_RAW_FD_FRAMES`, so both classic
  and FD frames flow.
- **RX:** a device frame → `struct can_frame` or `struct canfd_frame` written into
  the interface (with `CAN_EFF_FLAG` for extended IDs, `CANFD_BRS` for BRS).
- **TX:** frames you write to the socket are read by rexgend, converted to the
  device's internal record, and queued over USB for transmission.

The `vcan` module must be available in the kernel (`modprobe vcan` if not
built-in); on the RexGEN smart image it is present.

## 6. Receiving frames

Standard SocketCAN receive:
```c
int s = socket(PF_CAN, SOCK_RAW, CAN_RAW);

int enable = 1;
setsockopt(s, SOL_CAN_RAW, CAN_RAW_FD_FRAMES, &enable, sizeof(enable)); /* accept FD */

struct ifreq ifr;
strcpy(ifr.ifr_name, "can0");
ioctl(s, SIOCGIFINDEX, &ifr);

struct sockaddr_can addr = { .can_family = AF_CAN, .can_ifindex = ifr.ifr_ifindex };
bind(s, (struct sockaddr *)&addr, sizeof(addr));

struct canfd_frame f;
ssize_t n = read(s, &f, sizeof(f));   /* n == sizeof(can_frame) or sizeof(canfd_frame) */
```

Interpretation:
- `f.can_id & CAN_EFF_FLAG` → extended ID; mask with `CAN_EFF_MASK` (else `CAN_SFF_MASK`).
- `f.can_id & CAN_ERR_FLAG` → this is an **error frame** (see §9), not data.
- `n == sizeof(struct canfd_frame)` → an FD frame; `f.len` up to 64. Otherwise a
  classic frame (`f.len` ≤ 8).

## 7. Transmitting frames

Build a frame and `write()` it to the bound socket; rexgend transmits it via the
device:
```c
struct can_frame f = {0};
f.can_id  = 0x153;              /* | CAN_EFF_FLAG for an extended ID */
f.can_dlc = 8;
memcpy(f.data, (uint8_t[]){0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00,0x11}, 8);
write(s, &f, sizeof(f));
```
Extended ID: OR the identifier with `CAN_EFF_FLAG`. There is no per-frame
transmit ACK from the socket.

## 8. CAN FD

Enable FD on the socket (`CAN_RAW_FD_FRAMES`, as above) and use
`struct canfd_frame`:
```c
struct canfd_frame f = {0};
f.can_id = 0x12345678 | CAN_EFF_FLAG;   /* extended */
f.len    = 12;                          /* up to 64 */
f.flags  = CANFD_BRS;                   /* bit-rate switch */
/* fill f.data[0..len-1] */
write(s, &f, sizeof(f));
```
rexgend maps `CANFD_BRS` to the device's BRS bit and sends an FD frame.

## 9. Error frames

CAN bus errors appear as standard SocketCAN **error frames**: `can_id` has
`CAN_ERR_FLAG` set. Enable them with:
```c
can_err_mask_t mask = CAN_ERR_MASK;
setsockopt(s, SOL_CAN_RAW, CAN_RAW_ERR_FILTER, &mask, sizeof(mask));
```
Mapping used by rexgend:

| Device error         | SocketCAN encoding                                     |
|----------------------|--------------------------------------------------------|
| Bit Error            | `CAN_ERR_PROT`, `data[2] = CAN_ERR_PROT_BIT`           |
| Form Error           | `CAN_ERR_PROT`, `data[2] = CAN_ERR_PROT_FORM`          |
| Bit Stuffing Error   | `CAN_ERR_PROT`, `data[2] = CAN_ERR_PROT_STUFF`         |
| CRC Error            | `CAN_ERR_PROT`, `data[2] = CAN_ERR_PROT_BIT \| CAN_ERR_PROT_TX` |
| Acknowledgment Error | `CAN_ERR_ACK \| CAN_ERR_PROT`                          |

The device error code is placed in `data[5]` and the error count in `data[6]`.

## 10. Standard tools

Because these are ordinary Linux CAN interfaces, the usual utilities work:
```sh
candump can0                       # dump all frames (add -e for error frames)
candump any                        # all can* interfaces at once
cansend can0 153#AABBCCDDEEFF0011  # classic frame
cansend can0 12345678#DEADBEEF     # extended (8-digit ID)
cansend can0 123##1.AABBCC...      # CAN FD (## + flags nibble)
```
(`can-utils` package.)

## 11. Examples in this folder

`can_read` and `can_send` in **Bash**, **Python**, and **Node.js**:

```
bash/     can_read.sh   can_send.sh     # candump / cansend (can-utils)
python/   can_read.py   can_send.py     # stdlib socket + struct, no deps
nodejs/   can_read.js   can_send.js     # npm: socketcan  (+ package.json)
```

Run as root on the device (needs `use_socketcan = 1`):
```sh
# Bash — needs the can-utils package
sh bash/can_read.sh   can0
sh bash/can_send.sh   can0 153#AABBCCDDEEFF0011

# Python — standard library only
python3 python/can_read.py   can0
python3 python/can_send.py   can0 153 AA BB CC DD EE FF 00 11

# Node.js — install the native SocketCAN binding first
cd nodejs && npm install
node can_read.js   can0
node can_send.js   can0 153 AABBCCDDEEFF0011
```

Notes per language:
- **Bash** uses `candump`/`cansend` from `can-utils` (usually preinstalled).
- **Python** uses only `socket`/`struct` (no external package). For a richer API
  you can instead use `python-can`: `can.Bus(interface="socketcan", channel="can0")`.
- **Node.js** uses the `socketcan` npm package (native addon); `npm install`
  builds it. See `nodejs/package.json`.

## 12. Notes, limits, FAQ

- **Interface not found?** `use_socketcan = 0`, that CAN bus isn't in the config,
  or the `vcan` kernel module is missing (`modprobe vcan`). Check `ip link`.
- **FD vs classic:** enable `CAN_RAW_FD_FRAMES` and switch on the `read()` return
  size; otherwise the kernel delivers only classic frames and truncates FD ones.
- **Coexistence:** the CAN named pipes still exist and carry the same traffic; a
  frame appears on both, and sending via either path transmits once.
- **Timestamps:** use `SO_TIMESTAMP`/`SIOCGSTAMP` if you need kernel RX
  timestamps; the device's own millisecond timestamp is available in the
  named-pipe text form.
- **This is `vcan`, not `can`:** there is no real bitrate/bus-off state on the
  Linux side — bus timing lives in the logger. The vcan interface only shuttles
  frames to/from the device.

---

## 13. Verified On Real Hardware

Captured on a `REX18-A1-B003` unit over serial console, demonstrating both
paths against the same physical bus and the RexDesk bus configuration screen.

**RexDesk CAN0 settings** (`Configuration` → `CAN0` → `Settings` — bus speed,
mode; see [§4](#4-enabling-it) for `use_socketcan`):

![RexDesk CAN0 settings](../images/rexdesk-can-settings.jpg)

**Named-pipe send** (`echo ... > can0/tx`), reflected in RexDesk's live monitor:

```text
root@REX18-A1-B003-SN0000261:~# echo "(0) can0 100 [8] 11 22 33 44 55 66 77 88" > /var/run/rexgen/can0/tx
```

![Sending a CAN frame via the named pipe](../images/can-pipe-send.jpg)

**Named-pipe receive** (`cat can0/rx`):

```text
root@REX18-A1-B003-SN0000261:~# cat /var/run/rexgen/can0/rx
(135618812)  can0          100 [3] 00 00 00
(135619206)  can0          100 [3] 02 00 00
(135619617)  can0          100 [7] 04 00 00 00 00 00
```

![Receiving CAN frames via the named pipe](../images/can-pipe-receive.jpg)

**SocketCAN send** (`cansend`), the same bus as above:

```text
root@REX18-A1-B003-SN0000261:~# cansend can0 100#1122334455667788
```

![Sending a CAN frame with cansend](../images/can-socketcan-send.jpg)

**SocketCAN receive** (`candump`):

```text
root@REX18-A1-B003-SN0000261:~# candump can0
```

![Receiving CAN frames with candump](../images/can-socketcan-receive.jpg)

This confirms §2/§5 in practice: a frame sent via the named pipe (`can0/tx`) is
the same bus traffic seen by `candump`, and `cansend` traffic is the same bus
traffic seen on `can0/rx` — both interfaces are two views of one physical bus.
