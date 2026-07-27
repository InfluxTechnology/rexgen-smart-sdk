# Examples

`rexgend` bridges the Rexgen Core logger (over USB) to Linux user-space and exposes the live bus/sensor data through **two parallel mechanisms**:

1. **Named pipes (FIFOs)** — human-readable text, under `/var/run/rexgen/`. See [named-pipes/](named-pipes/README.md).
2. **SocketCAN (vcan)** — standard Linux virtual CAN interfaces (`can0`..`can3`), usable with `candump`/`cansend` and any SocketCAN program. See [socketcan/](socketcan/README.md).

Both are active at the same time when SocketCAN is enabled: a CAN frame from the device shows up **both** in the `canN/rx` pipe **and** on the `canN` vcan socket, and a frame you send through **either** path is transmitted by the device. This is verified on real hardware in both folders' "Verified On Real Hardware" sections.

Sensors (GNSS, accelerometer, gyroscope, digital inputs, ADC) are **named pipes only** — there is no SocketCAN equivalent for them.

## Layout

```text
named-pipes/                     socketcan/
├── README.md   (full spec)      ├── README.md   (full spec)
├── bash/       *.sh             ├── bash/        *.sh   (candump / cansend)
├── python/     *.py             ├── python/      *.py   (stdlib socket)
└── nodejs/     *.js             └── nodejs/      *.js   (npm: socketcan)
images/                          (screenshots referenced by both READMEs)
```

| Task        | Named pipes                        | SocketCAN                         |
|-------------|-------------------------------------|-----------------------------------|
| read CAN    | `can_read.{sh,py,js}`              | `can_read.{sh,py,js}`             |
| send CAN    | `can_send.{sh,py,js}`              | `can_send.{sh,py,js}`             |
| read GNSS   | `gnss_read.{sh,py,js}`             | — (pipes only)                    |
| read GPIO / digital in | `gpio_read.{sh,py,js}` (reusable for acc/gyro/adc) | — (pipes only) |

## Quick Start

Run on the device as `root` (`/var/run/rexgen` and the CAN interfaces are root-owned):

```sh
# Bash
sh named-pipes/bash/can_read.sh   can0
sh socketcan/bash/can_read.sh     can0        # needs can-utils

# Python (stdlib only)
python3 named-pipes/python/can_read.py   can0
python3 socketcan/python/can_read.py     can0

# Node.js
node named-pipes/nodejs/can_read.js   can0
cd socketcan/nodejs && npm install && node can_read.js can0   # needs the socketcan pkg
```

See [named-pipes/README.md](named-pipes/README.md) and [socketcan/README.md](socketcan/README.md) for the complete specification: pipe/interface paths, text and binary frame formats, GNSS channel list, error frames, `use_socketcan` configuration, and known gotchas.
