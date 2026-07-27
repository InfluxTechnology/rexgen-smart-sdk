#!/bin/sh
# Read GNSS (GPS) channels from the rexgend named pipe.
#   usage: ./gnss_read.sh
#
# Each line:  (timestamp) <channel> <value>
# Channels: Latitude, Longitude (double), Altitude, SpeedOverGround, ...,
#           Datetime (uint32 Unix epoch seconds).

PIPE="/var/run/rexgen/gnss/rx"
[ -p "$PIPE" ] || { echo "no pipe $PIPE (GNSS configured?)" >&2; exit 1; }

# Stream everything:
cat "$PIPE"

# Or pick one channel, e.g. latitude/longitude only:
#   cat "$PIPE" | awk '$2=="Latitude" || $2=="Longitude" { print }'
#
# Or reshape "(ts) Latitude 43.57" -> "ts=... Latitude=...":
#   cat "$PIPE" | sed -E 's/^\(([0-9]+)\) ([^ ]+) (.*)$/ts=\1 \2=\3/'
