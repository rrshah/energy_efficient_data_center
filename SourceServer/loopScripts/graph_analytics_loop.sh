#!/bin/bash

echo "Creating Data Directory for Graph Analytics."
docker create --name data-graph-analytics cloudsuite/twitter-dataset-graph

echo "Starting Graph Analytics Looped Execution"

while true; do
	echo "Begin..."
	sudo docker run --rm --name graph-server --volumes-from data-graph-analytics cloudsuite/graph-analytics --driver-memory 2g --executor-memory 8g

	echo "End..."
done

