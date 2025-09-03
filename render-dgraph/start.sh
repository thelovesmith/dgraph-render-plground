#!/bin/bash

# Start Dgraph Zero in the background
dgraph zero --config /dgraph/config/dgraph-config.yml &

# Wait a moment for Zero to start
sleep 5

# Start Dgraph Alpha
dgraph alpha --config /dgraph/config/dgraph-config.yml &

# Wait for all processes to finish
wait
