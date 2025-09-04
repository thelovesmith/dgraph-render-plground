#!/bin/bash

# Set Dgraph Alpha security token from environment variable
#if [ -n "$DGRAPH_TOKEN" ]; then
#    export DGRAPH_ALPHA_SECURITY="whitelist=0.0.0.0/0;token=$DGRAPH_TOKEN"
#    echo "Security token configured for Dgraph Alpha"
#    echo "DGRAPH_ALPHA_SECURITY=$DGRAPH_ALPHA_SECURITY"
#else
#    export DGRAPH_ALPHA_SECURITY="whitelist=0.0.0.0/0"
#    echo "Warning: DGRAPH_TOKEN not set, running without security"
#fi
export DGRAPH_ALPHA_SECURITY="whitelist=0.0.0.0/0"
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
