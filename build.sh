#!/bin/sh
#
# Run this in firmware's top directory.
# Builds build container and runs build-entrypoint.sh that builds the new firmware.
#
docker build --pull --rm -t card10build -f docker/build-env/Dockerfile .
exec docker run --rm --mount type=bind,source=${PWD},destination=/build card10build /build/build-entrypoint.sh

