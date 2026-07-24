# Example: GNSS Data

Rexgen Smart's GNSS receiver can be read two ways: a parsed, field-per-line Rexgen pipe, or the raw NMEA 0183 sentences straight off the GNSS module's UART.

## Init Hardware

The GNSS receiver needs to be started before either path produces data:

```text
root@REX18-A1-B003-SN0000261:~# /opt/influx/gnssdata_start.sh
```

Run this once per boot (or after a GNSS module reset) before reading `gnss/rx` or `/dev/ttymxc1`.

## Method 1: Parsed Pipe

```text
root@REX18-A1-B003-SN0000261:~# cat /var/run/rexgen/gnss/rx
(1235271491) Longitude 27.827378
(1235271540) GeoidSeparation 36.000000
(1235271565) NumberSatellites 5.000000
(1235271589) Quality 1.000000
(1235272766) CourseOverGround 146.100006
(1235371846) Latitude 43.571451
(1235371915) Altitude 209.000000
(1235371941) GeoidSeparation 36.000000
(1235371965) NumberSatellites 5.000000
(1235371982) Quality 1.000000
(1235372946) Latitude 43.571451
(1235373001) SpeedOverGround 0.300000
(1235373027) CourseOverGround 13.700000
```

Each line is `(timestamp) <field> <value>`. Fields arrive incrementally as the receiver updates them — a full fix's fields (`Latitude`, `Longitude`, `Altitude`, `Quality`, `NumberSatellites`, `GeoidSeparation`, `SpeedOverGround`, `CourseOverGround`) are not guaranteed on the same line and should be accumulated by a consumer, keyed by field name, with the latest value per field.

![GNSS parsed pipe](images/gnss-pipe.jpg)

## Method 2: Raw UART (NMEA 0183)

```text
root@REX18-A1-B003-SN0000261:~# cat /dev/ttymxc1
$GPGSV,3,1,12,03,66,074,26,04,72,264,25,06,26,313,28,07,04,194,24,1*67
$GPGSV,3,2,12,09,36,250,25,17,14,251,22,19,16,284,20,26,09,091,29,1*62
$GPGSV,3,3,12,31,34,056,22,01,33,167,,02,10,164,,28,11,037,,1*6E
$GPGGA,114506.00,4334.297554,N,02749.644530,E,1,05,1.0,192.8,M,36.0,M,,*68
$GPVTG,21.7,T,17.7,M,0.0,N,0.0,K,A*26
$GPRMC,114506.00,A,4334.297554,N,02749.644530,E,0.0,21.7,220726,4.0,E,A,V*7B
$GPGSA,A,3,06,09,17,19,26,,,,,,,1.3,1.0,0.9,1*20
```

This is the unprocessed NMEA 0183 stream from the GNSS module — standard sentences (`$GPGSV` satellites in view, `$GPGGA` fix data, `$GPVTG` course/speed over ground, `$GPRMC` recommended minimum data, `$GPGSA` DOP/active satellites). Use this path if you need sentences the parsed pipe doesn't expose, or want to run your own NMEA parser (e.g. `gpsd`, `libnmea`).

![GNSS raw UART](images/gnss-uart.jpg)

## Notes

- `/dev/ttymxc1` is the raw serial device for the GNSS module on this board revision — confirm the exact device node for your hardware revision if it differs.
- `Quality 1` in the parsed pipe corresponds to `$GPGGA`'s fix-quality field (`1` = GPS fix, no correction); `NumberSatellites 5` matches the satellite count used in the fix.
- Prefer the parsed pipe (`gnss/rx`) for application code that just needs position/speed/course; use the raw UART only if you need sentence-level detail or want to run your own parser.
