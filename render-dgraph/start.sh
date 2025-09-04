#!/bin/bash

# Start Dgraph Zero in the background
dgraph zero --config /dgraph/config/dgraph-config.yml &

# Wait a moment for Zero to start
sleep 5

# Start Dgraph Alpha
dgraph alpha --config /dgraph/config/dgraph-config.yml &

# Keep the container running indefinitely
# This prevents the container from exiting even if dgraph processes are killed
# Using tail -f /dev/null is more efficient than while true loop
tail -f /dev/null
