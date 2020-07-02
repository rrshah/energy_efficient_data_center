#!/bin/bash

echo "Creating Network for Data Analytics..."
sudo docker network create hadoop-net

echo "Starting Master..."
sudo docker run -d --net hadoop-net --name data-analytics-master --hostname data-analytics-master cloudsuite/data-analytics master

echo "Starting Slave..."
sudo docker run -d --net hadoop-net --name data-analytics-slave01 --hostname data-analytics-slave01 cloudsuite/hadoop slave
sudo docker run -d --net hadoop-net --name data-analytics-slave02 --hostname data-analytics-slave01 cloudsuite/hadoop slave
sudo docker run -d --net hadoop-net --name data-analytics-slave03 --hostname data-analytics-slave01 cloudsuite/hadoop slave
sudo docker run -d --net hadoop-net --name data-analytics-slave04 --hostname data-analytics-slave01 cloudsuite/hadoop slave

echo "Starting Data Analytics Looped Execution"

while true; do
	echo "Begin..."
	sudo docker exec data-analytics-master benchmark
	echo "End..."
done
