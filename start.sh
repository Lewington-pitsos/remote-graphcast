#!/bin/bash

echo "graphcast pod start script running..."

python -m remote_graphcast.cast 

while true; do
	echo "finished, $(date)"
	sleep 30
done
