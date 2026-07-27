#!/bin/sh
# Read digital inputs (GPIO) from the rexgend named pipe.
#   usage: ./gpio_read.sh
#
# Each line:  (timestamp) <channel> <state>   e.g. "(1699999999) 0 1"
# Digital I/O is READ-ONLY through rexgend (no GPIO output pipe).
#
# The same works for acc/gyro/adc by changing the pipe (values are floats):
#   /var/run/rexgen/acc/rx  /var/run/rexgen/gyro/rx  /var/run/rexgen/adc/rx

PIPE="/var/run/rexgen/dig/rx"
[ -p "$PIPE" ] || { echo "no pipe $PIPE (digital configured?)" >&2; exit 1; }

cat "$PIPE"

# Print only rising edges of channel 0:
#   cat "$PIPE" | awk '$2=="0" && $3=="1" { print }'
