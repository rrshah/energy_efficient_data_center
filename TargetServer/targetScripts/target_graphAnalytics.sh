#!/bin/bash
echo 'Running Graph Analytics on Kraken....'
containername="$1"

echo "Stopping container if running..."
sudo docker stop $containername

echo "Removing container..."
sudo docker rm $containername

echo "Removing container image..."
sudo docker image rm ${containername}_image

echo "Loading previously saved container..."
sudo docker load < /home/sjsu_ra/migration_img/${containername}_image.tar

#echo "Creating Dataset Image..."
#sudo docker create --name data-graph-analytics cloudsuite/twitter-dataset-graph

echo "Running loaded container..."
/home/sjsu_ra/migration_new/loopScripts/graph_analytics_loop.sh


now=$(date +"%T")
echo "End time : :$now"

