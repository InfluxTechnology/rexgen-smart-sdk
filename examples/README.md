# Examples

Working, device-verified examples for reading and writing Rexgen Smart data from Linux userspace. Each example was captured on a real `imx8mm-smart` unit (`REX18-A1-B003`) over a serial console.

| Example | What it covers |
|---|---|
| [can.md](can.md) | Sending and receiving CAN frames, two ways: the Rexgen named-pipe interface and standard Linux SocketCAN (`cansend`/`candump`) |
| [sensor-channels.md](sensor-channels.md) | Reading Accelerometer, Gyroscope, Analog (ADC), and Digital input channels; enabling channels with RexDesk |
| [gnss.md](gnss.md) | Reading parsed GNSS fixes and raw NMEA UART output |

## Common Pattern: The Rexgen Pipe Interface

Most of these examples read from named pipes under `/var/run/rexgen/<channel>/rx` (and, for CAN, write to `/var/run/rexgen/<channel>/tx`). Each line is timestamped:

```text
(<timestamp>) <field or channel index> <value>
```

`<timestamp>` is a monotonically increasing counter (microseconds since some device-internal epoch, not wall-clock time) — use it to order/deduplicate samples, not to derive real-world time.

## Enabling Channels

Before a `/var/run/rexgen/<channel>/rx` pipe produces data, the corresponding channel must be enabled on the device. This is done from **RexDesk** (`Configuration` panel → `Channels` / `Logging`), not from the Linux shell — see [sensor-channels.md](sensor-channels.md#enabling-channels-with-rexdesk) and [can.md](can.md#configuring-the-can-bus-with-rexdesk) for the exact screens.
