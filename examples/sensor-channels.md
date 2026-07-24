# Example: Accelerometer, Gyroscope, Analog (ADC), And Digital Channels

Rexgen Smart exposes its onboard IMU (accelerometer + gyroscope) and its analog/digital I/O channels as named pipes under `/var/run/rexgen/`. All four follow the same read pattern; only the enabled-channel configuration and units differ.

## Enabling Channels With RexDesk

Channels must be enabled in a RexDesk project's `Configuration` panel before their pipes produce data. The relevant tools are under `Tools` → `Channels` (`Analog`, `Dig In`, `Accel`, `Gyro`, `GNSS`), which populate the `Channels` section of `Configuration`:

![RexDesk Channels configuration](images/rexdesk-channels.jpg)

Enable the channels you need (Accel/Gyro/Analog/Dig In/GNSS), then push the configuration to the device (`Run` / `Live`) before reading the pipes below.

## Accelerometer

```text
root@REX18-A1-B003-SN0000261:~# cat /var/run/rexgen/acc/rx
(1993525684) X 0.009760
(1993525684) Y -0.011712
(1993525684) Z 1.003816
(1993535687) X 0.012688
(1993535687) Y -0.007320
(1993535687) Z 1.000400
(1993545690) X 0.010736
(1993545690) Y -0.011224
(1993545690) Z 1.001864
```

Values are in **g** (note `Z ≈ 1.0` at rest — gravity on a stationary, level device).

## Gyroscope

```text
root@REX18-A1-B003-SN0000261:~# cat /var/run/rexgen/gyro/rx
(1994245964) X -0.297500
(1994245964) Y 0.455000
(1994245964) Z -0.315000
(1994255966) X -0.367500
(1994255966) Y 0.525000
(1994255966) Z -0.280000
```

Values are in **degrees/second**. Small non-zero readings at rest are normal sensor noise/bias.

![Accelerometer and gyroscope pipes](images/acc-gyro-pipe.jpg)

## Analog (ADC) Channels

```text
root@REX18-A1-B003-SN0000261:~# cat /var/run/rexgen/adc/rx
(2004153740) 3 12.123950
(2004156306) 0 0.047500
(2004162562) 1 0.025000
(2004162747) 2 0.062500
(2004163742) 3 12.056001
(2004166312) 0 0.047500
```

Each line is `(timestamp) <channel index> <voltage>`. In this capture, channel `3` reads ~12V (a supply/battery-monitor input) while channels `0`–`2` read near-zero (floating/unconnected analog inputs) — connect a real signal to see a channel move.

## Digital Input Channels

```text
root@REX18-A1-B003-SN0000261:~# cat /var/run/rexgen/dig/rx
(2004895024) 2 1
(2004896042) 3 1
(2004897664) 0 1
(2004899673) 1 1
(2004905027) 2 1
```

Each line is `(timestamp) <channel index> <state>` (`0`/`1`).

![ADC and digital input pipes](images/adc-dig-pipe.jpg)

## Notes

- Channel indices (`0`–`3` above) correspond to the physical Analog/Digital connector pins for this hardware revision — confirm the exact pin mapping for your board revision before wiring a real signal.
- These pipes are read-only telemetry streams; there is no corresponding `tx` pipe for Accel/Gyro/ADC/Dig (unlike CAN, which is bidirectional — see [can.md](can.md)).
- For application code, treat each `cat`-able pipe as a line-oriented stream: open it, read lines, parse `(timestamp) field value`, and keep reading — it does not EOF while the channel is enabled and running.
