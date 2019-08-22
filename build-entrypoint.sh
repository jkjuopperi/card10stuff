#!/bin/sh
#
# This is run inside build container to build the firmware.
#
set -e
set -x

cd /build
./bootstrap.sh
ninja -C build/
