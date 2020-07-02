#!/bin/bash
echo 'Running Data Analytics on Kraken....'
containername="$1"

echo "Stopping container if running..."
sudo docker stop $containername

echo "Removing container..."
sudo docker rm -f $containername data-analytics-master data-analytics-slave01 data-analytics-slave02 data-analytics-slave03 data-analytics-slave04

echo "Removing container image..."
sudo docker image rm ${containername}_image data-analytics-master data-analytics-slave01 data-analytics-slave02 data-analytics-slave03 data-analytics-slave04

echo "Loading previously saved container..."
sudo docker load < /home/sjsu_ra/migration_img/${containername}_image.tar

echo "Running loaded container..."
sudo  docker run -d --net hadoop-net --name data-analytics-master --hostname data-analytics-master cloudsuite/data-analytics master
sudo docker run -d --net hadoop-net --name data-analytics-slave01 --hostname data-analytics-slave01 cloudsuite/hadoop slave
sudo docker run -d --net hadoop-net --name data-analytics-slave03 --hostname data-analytics-slave03 cloudsuite/hadoop slave
sudo docker run -d --net hadoop-net --name data-analytics-slave04 --hostname data-analytics-slave04 cloudsuite/hadoop slave
sudo docker run -d --net hadoop-net --name data-analytics-slave02 --hostname data-analytics-slave02 cloudsuite/hadoop slave
sudo docker exec data-analytics-master benchmark

now=$(date +"%T")
echo "End time : :$now"
